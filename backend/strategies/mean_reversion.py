import pandas as pd


class MeanReversion:
    """
    Mean reversion strategy.

    BUY when price < SMA20 - k * std
    SELL when price > SMA20
    """

    def __init__(self, window: int = 20, std_k: float = 2.0):
        self.window = window
        self.std_k = std_k

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        close = df["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        sma = close.rolling(self.window).mean()
        std = close.rolling(self.window).std()
        lower_band = sma - self.std_k * std

        df["SMA"] = sma
        df["STD"] = std

        df["Signal"] = 0
        # Enter long when price is significantly below SMA
        df.loc[close < lower_band, "Signal"] = 1
        # Exit when price is back above SMA
        df.loc[close > sma, "Signal"] = 0

        df["Position"] = df["Signal"].ffill().fillna(0)
        return df


