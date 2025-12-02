import pandas as pd


class MACrossover:
    """
    Simple moving average crossover strategy.

    BUY when fast MA > slow MA
    SELL when fast MA < slow MA
    """

    def __init__(self, fast: int = 20, slow: int = 50):
        if fast >= slow:
            raise ValueError("fast period must be less than slow period")
        self.fast = fast
        self.slow = slow

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        close = df["Close"]
        # robust in case "Close" is returned as single-column DataFrame
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        df["MA_fast"] = close.rolling(self.fast).mean()
        df["MA_slow"] = close.rolling(self.slow).mean()

        df["Signal"] = 0
        df.loc[df["MA_fast"] > df["MA_slow"], "Signal"] = 1
        df.loc[df["MA_fast"] < df["MA_slow"], "Signal"] = -1

        # Position is last signal (no intraday switching)
        df["Position"] = df["Signal"]
        return df


