from datetime import date
from typing import Literal, Optional, List

from fastapi import APIRouter
from pydantic import BaseModel

from ..data.fetch import get_ohlcv


class DataRequest(BaseModel):
    ticker: str
    source: Literal["yfinance", "ccxt"] = "yfinance"
    start: date
    end: date
    interval: str = "1d"


router = APIRouter()

SUPPORTED_TICKERS = [
    {"symbol": "AAPL", "type": "stock", "description": "Apple Inc."},
    {"symbol": "MSFT", "type": "stock", "description": "Microsoft Corporation"},
    {"symbol": "GOOG", "type": "stock", "description": "Alphabet Inc. (Google)"},
    {"symbol": "SPY", "type": "etf", "description": "SPDR S&P 500 ETF"},
    {"symbol": "BTC-USD", "type": "crypto", "description": "Bitcoin vs USD (yfinance)"},
]


@router.get(
    "/tickers",
    summary="Список преднастроенных тикеров",
    description="Возвращает список доступных в UI тикеров с кратким описанием.",
)
def get_tickers() -> List[dict]:
    return SUPPORTED_TICKERS


@router.post(
    "/load",
    summary="Загрузить исторические данные",
    description="Загружает OHLCV для выбранного тикера из yfinance/ccxt с учётом кэша.",
)
def load_data(req: DataRequest):
    df = get_ohlcv(
        ticker=req.ticker,
        start=req.start,
        end=req.end,
        source=req.source,
        interval=req.interval,
    )
    return {
        "ticker": req.ticker,
        "source": req.source,
        "interval": req.interval,
        "rows": len(df),
        "start": df.index.min().isoformat() if not df.empty else None,
        "end": df.index.max().isoformat() if not df.empty else None,
    }


