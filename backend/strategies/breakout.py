import pandas as pd


class Breakout:
    """
    Breakout strategy.

    BUY: price > max(high, N days)
    SELL: price < min(low, N days)
    """

    def __init__(self, window: int = 20):
        self.window = window

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        high = df["High"]
        low = df["Low"]
        close = df["Close"]

        if isinstance(high, pd.DataFrame):
            high = high.iloc[:, 0]
        if isinstance(low, pd.DataFrame):
            low = low.iloc[:, 0]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        high_max = high.rolling(self.window).max()
        low_min = low.rolling(self.window).min()

        df["High_max"] = high_max
        df["Low_min"] = low_min

        df["Signal"] = 0
        df.loc[close > high_max.shift(1), "Signal"] = 1
        df.loc[close < low_min.shift(1), "Signal"] = 0

        df["Position"] = df["Signal"].ffill().fillna(0)
        return df


