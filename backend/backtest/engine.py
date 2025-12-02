from dataclasses import dataclass

import pandas as pd


@dataclass
class BacktestEngine:
    data: pd.DataFrame
    strategy: object
    initial_capital: float = 10_000.0

    def run(self) -> pd.DataFrame:
        df = self.strategy.generate_signals(self.data.copy())

        if "Position" not in df.columns:
            raise ValueError("Strategy must produce 'Position' column")

        df["Returns"] = df["Close"].pct_change().fillna(0.0)
        df["Strategy"] = df["Position"].shift(1).fillna(0.0) * df["Returns"]

        df["Equity"] = (1.0 + df["Strategy"]).cumprod() * self.initial_capital

        # Generate basic trade log info
        df["Position_change"] = df["Position"].diff().fillna(df["Position"])
        return df


