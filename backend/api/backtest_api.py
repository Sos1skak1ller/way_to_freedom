from datetime import date
from typing import Any, Dict, Literal, Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..backtest.engine import BacktestEngine
from ..backtest.metrics import compute_metrics, extract_trades
from ..data.fetch import get_ohlcv
from ..strategies.ma_crossover import MACrossover
from ..strategies.mean_reversion import MeanReversion
from ..strategies.breakout import Breakout
from ..utils.plot import equity_plot, price_signals_plot


class Period(BaseModel):
    start: date
    end: date


class BacktestRequest(BaseModel):
    ticker: str
    strategy: Literal["ma_crossover", "mean_reversion", "breakout"]
    params: Dict[str, Any] = {}
    period: Period
    source: Literal["yfinance", "ccxt"] = "yfinance"
    interval: str = "1d"
    initial_capital: float = 10_000


router = APIRouter()

STRATEGIES_INFO = [
    {
        "name": "ma_crossover",
        "label": "MA Crossover",
        "description": "Стратегия пересечения скользящих средних. Fast MA > Slow MA — вход в лонг, Fast MA < Slow MA — выход.",
        "params": {
            "fast": "длина быстрой скользящей средней в днях",
            "slow": "длина медленной скользящей средней в днях",
        },
    },
    {
        "name": "mean_reversion",
        "label": "Mean Reversion",
        "description": "Стратегия возврата к среднему. Покупка при отклонении цены ниже SMA - k*std, выход при возврате выше SMA.",
        "params": {
            "window": "размер окна в днях для SMA и стандартного отклонения",
            "std_k": "во сколько стандартных отклонений цена должна уйти ниже средней",
        },
    },
    {
        "name": "breakout",
        "label": "Breakout",
        "description": "Стратегия пробоя диапазона. Вход при пробое максимума за N дней, выход при уходе ниже минимума.",
        "params": {
            "window": "размер окна в днях для поиска локальных максимумов и минимумов",
        },
    },
]


@router.get(
    "/strategies",
    summary="Список доступных стратегий",
    description="Возвращает стратегии, их краткое описание и параметры, которые можно настраивать.",
)
def list_strategies() -> List[dict]:
    return STRATEGIES_INFO


def _get_strategy(name: str, params: Dict[str, Any]):
    if name == "ma_crossover":
        return MACrossover(**params)
    if name == "mean_reversion":
        return MeanReversion(**params)
    if name == "breakout":
        return Breakout(**params)
    raise ValueError(f"Unknown strategy: {name}")


@router.post(
    "/run",
    summary="Запуск бэктеста стратегии",
    description="Запускает бэктест выбранной стратегии на исторических данных и возвращает equity, сделки и метрики.",
)
def run_backtest(req: BacktestRequest):
    df = get_ohlcv(
        ticker=req.ticker,
        start=req.period.start,
        end=req.period.end,
        source=req.source,
        interval=req.interval,
    )
    if df.empty:
        raise HTTPException(status_code=400, detail="No data for given parameters")

    strategy = _get_strategy(req.strategy, req.params)
    engine = BacktestEngine(df, strategy, initial_capital=req.initial_capital)
    result_df = engine.run()

    metrics = compute_metrics(result_df["Strategy"].dropna(), freq="D")
    trades = extract_trades(result_df)

    # Equity as plain list of floats
    equity_series = result_df["Equity"]
    equity = equity_series.to_numpy().tolist()

    labels = [idx.isoformat() for idx in result_df.index]

    # Close price as list (robust to possible single-column DataFrame)
    close_values = result_df["Close"]
    close_arr = getattr(close_values, "to_numpy")()
    if close_arr.ndim > 1:
        close_arr = close_arr[:, 0]
    price = close_arr.tolist()

    # Signals as list (0/1/-1)
    if "Signal" in result_df.columns:
        sig_values = result_df["Signal"]
        sig_arr = getattr(sig_values, "to_numpy")()
        if sig_arr.ndim > 1:
            sig_arr = sig_arr[:, 0]
        signals = sig_arr.tolist()
    else:
        signals = []

    equity_png = equity_plot(equity, labels)
    price_png = price_signals_plot(price, labels, signals) if signals else None

    return {
        "equity": equity,
        "labels": labels,
        "price": price,
        "signals": signals,
        "metrics": metrics,
        "trades": trades,
        "equity_png": equity_png,
        "price_png": price_png,
    }


