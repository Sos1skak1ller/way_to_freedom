from typing import Dict, List

import math
import numpy as np
import pandas as pd


def _annualization_factor(freq: str) -> float:
    freq = freq.upper()
    if freq == "D":
        return 252.0
    if freq in {"H", "1H"}:
        return 252.0 * 6.5  # intraday hours approximation
    if freq in {"M", "1M"}:
        return 12.0
    return 252.0


def sharpe_ratio(returns: pd.Series, freq: str = "D", rf: float = 0.0) -> float:
    if returns.empty:
        return float("nan")
    ex_ret = returns - rf / _annualization_factor(freq)
    std = ex_ret.std()
    if std == 0:
        return float("nan")
    return np.sqrt(_annualization_factor(freq)) * ex_ret.mean() / std


def sortino_ratio(returns: pd.Series, freq: str = "D", rf: float = 0.0) -> float:
    if returns.empty:
        return float("nan")
    ex_ret = returns - rf / _annualization_factor(freq)
    downside = ex_ret[ex_ret < 0]
    if downside.std() == 0:
        return float("nan")
    return np.sqrt(_annualization_factor(freq)) * ex_ret.mean() / downside.std()


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return float("nan")
    cum_max = equity.cummax()
    dd = equity / cum_max - 1.0
    return dd.min()


def cagr(equity: pd.Series, freq: str = "D") -> float:
    if equity.empty:
        return float("nan")
    n_periods = len(equity)
    if n_periods <= 1:
        return float("nan")
    ann_factor = _annualization_factor(freq)
    years = n_periods / ann_factor
    if years <= 0:
        return float("nan")
    return (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1


def volatility(returns: pd.Series, freq: str = "D") -> float:
    if returns.empty:
        return float("nan")
    return returns.std() * np.sqrt(_annualization_factor(freq))


def win_rate(returns: pd.Series) -> float:
    if returns.empty:
        return float("nan")
    wins = (returns > 0).sum()
    total = (returns != 0).sum()
    if total == 0:
        return float("nan")
    return wins / total


def profit_factor(returns: pd.Series) -> float:
    if returns.empty:
        return float("nan")
    gains = returns[returns > 0].sum()
    losses = -returns[returns < 0].sum()
    if losses == 0:
        # Undefined / no losses -> treat as NaN to avoid JSON inf
        return float("nan")
    return gains / losses


def _to_json_number(x) -> float | None:
    """
    Convert value to JSON-safe float (no NaN/inf). Returns None if not finite.
    """
    if x is None:
        return None
    try:
        val = float(x)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(val):
        return None
    return val


def compute_metrics(returns: pd.Series, freq: str = "D") -> Dict[str, float]:
    """
    Compute main performance metrics from strategy returns.
    """
    equity = (1.0 + returns.fillna(0.0)).cumprod()
    raw = {
        "sharpe": sharpe_ratio(returns, freq=freq),
        "sortino": sortino_ratio(returns, freq=freq),
        "max_drawdown": max_drawdown(equity),
        "cagr": cagr(equity, freq=freq),
        "volatility": volatility(returns, freq=freq),
        "win_rate": win_rate(returns),
        "profit_factor": profit_factor(returns),
    }
    # Sanitize for JSON (no NaN/inf)
    return {k: _to_json_number(v) for k, v in raw.items()}


def extract_trades(df: pd.DataFrame) -> List[Dict]:
    """
    Simple trade extraction from Position changes.
    Assumes long-only or flat (0/1) positions for now.
    """
    trades: List[Dict] = []
    position = df["Position"].fillna(0)
    pos_change = position.diff().fillna(position)

    current_trade = None
    for dt, row in df.iterrows():
        change = pos_change.loc[dt]
        price = row["Close"]
        # row["Close"] can be a Series (e.g. from duplicate/MultiIndex columns)
        if hasattr(price, "iloc"):
            price = price.iloc[0]
        price = float(price)
        if change > 0:  # enter long
            current_trade = {
                "entry_date": dt.isoformat(),
                "entry_price": price,
                "exit_date": None,
                "exit_price": None,
                "return": None,
                "type": "LONG",
            }
        elif change < 0 and current_trade is not None:
            current_trade["exit_date"] = dt.isoformat()
            current_trade["exit_price"] = price
            current_trade["return"] = float(
                (current_trade["exit_price"] / current_trade["entry_price"]) - 1.0
            )
            trades.append(current_trade)
            current_trade = None

    return trades


