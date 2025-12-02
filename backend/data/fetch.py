import os
from datetime import date, datetime
from typing import Literal

import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover - optional for now
    yf = None

try:
    import ccxt  # type: ignore
except ImportError:  # pragma: no cover
    ccxt = None


CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(
    ticker: str,
    start: date,
    end: date,
    source: str,
    interval: str,
) -> str:
    safe_ticker = ticker.replace("/", "_").upper()
    fname = f"{source}_{safe_ticker}_{start.isoformat()}_{end.isoformat()}_{interval}.parquet"
    return os.path.join(CACHE_DIR, fname)


def _load_from_cache(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    try:
        df = pd.read_parquet(path)
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        return df
    except Exception:
        return pd.DataFrame()


def _save_to_cache(df: pd.DataFrame, path: str) -> None:
    try:
        df.to_parquet(path)
    except Exception:
        pass


def _fetch_yfinance(ticker: str, start: date, end: date, interval: str) -> pd.DataFrame:
    if yf is None:
        raise RuntimeError("yfinance is not installed")
    data = yf.download(
        ticker,
        start=start.isoformat(),
        end=end.isoformat(),
        interval=interval,
        auto_adjust=False,
        progress=False,
    )
    if data.empty:
        return pd.DataFrame()
    data = data.rename(
        columns={
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Adj Close": "AdjClose",
            "Volume": "Volume",
        }
    )
    data.index = pd.to_datetime(data.index)
    return data[["Open", "High", "Low", "Close", "Volume"]]


def _fetch_ccxt(
    ticker: str,
    start: date,
    end: date,
    interval: str,
    exchange_name: str = "binance",
) -> pd.DataFrame:
    if ccxt is None:
        raise RuntimeError("ccxt is not installed")

    # Map simple interval strings to ccxt timeframes
    timeframe_map = {
        "1d": "1d",
        "4h": "4h",
        "1h": "1h",
        "1m": "1m",
    }
    timeframe = timeframe_map.get(interval, "1d")

    exchange_cls = getattr(ccxt, exchange_name)
    exchange = exchange_cls()

    since = int(datetime.combine(start, datetime.min.time()).timestamp() * 1000)
    until_ts = int(datetime.combine(end, datetime.min.time()).timestamp() * 1000)

    all_ohlcv = []
    limit = 1000
    while since < until_ts:
        batch = exchange.fetch_ohlcv(ticker, timeframe=timeframe, since=since, limit=limit)
        if not batch:
            break
        all_ohlcv.extend(batch)
        since = batch[-1][0] + 1

    if not all_ohlcv:
        return pd.DataFrame()

    df = pd.DataFrame(
        all_ohlcv, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.set_index("timestamp")
    return df[["Open", "High", "Low", "Close", "Volume"]]


def get_ohlcv(
    ticker: str,
    start: date,
    end: date,
    source: Literal["yfinance", "ccxt"] = "yfinance",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Get OHLCV data with Parquet caching.
    """
    path = _cache_path(ticker=ticker, start=start, end=end, source=source, interval=interval)
    df = _load_from_cache(path)
    if not df.empty:
        # Filter to exact period
        df = df.loc[(df.index.date >= start) & (df.index.date <= end)]
        return df

    if source == "yfinance":
        df = _fetch_yfinance(ticker, start, end, interval)
    elif source == "ccxt":
        df = _fetch_ccxt(ticker, start, end, interval)
    else:
        raise ValueError(f"Unknown data source: {source}")

    if not df.empty:
        _save_to_cache(df, path)
    return df


