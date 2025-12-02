import base64
from io import BytesIO
from typing import Iterable, List

import matplotlib.pyplot as plt


def _fig_to_base64() -> str:
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def equity_plot(equity: Iterable[float], labels: List[str]) -> str:
    plt.figure(figsize=(8, 3))
    plt.plot(labels, equity, label="Equity")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    return _fig_to_base64()


def price_signals_plot(
    price: Iterable[float],
    labels: List[str],
    signals: Iterable[int],
) -> str:
    price = list(price)
    labels = list(labels)
    signals = list(signals)

    plt.figure(figsize=(8, 3))
    plt.plot(labels, price, label="Price", color="black")

    buy_x = [labels[i] for i, s in enumerate(signals) if s == 1]
    buy_y = [price[i] for i, s in enumerate(signals) if s == 1]
    sell_x = [labels[i] for i, s in enumerate(signals) if s == -1]
    sell_y = [price[i] for i, s in enumerate(signals) if s == -1]

    if buy_x:
        plt.scatter(buy_x, buy_y, marker="^", color="green", label="BUY")
    if sell_x:
        plt.scatter(sell_x, sell_y, marker="v", color="red", label="SELL")

    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    return _fig_to_base64()


