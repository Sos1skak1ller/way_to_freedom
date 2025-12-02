import React from "react";

export function TickerSelect({ value, onChange }) {
  const options = ["AAPL", "MSFT", "GOOG", "SPY", "BTC-USD"];

  return (
    <div className="field">
      <label
        title={
          "Тикер — инструмент, по которому строится бэктест. " +
          "AAPL, MSFT, GOOG — отдельные акции; SPY — ETF на индекс S&P 500; BTC-USD — Bitcoin к доллару."
        }
      >
        Ticker
      </label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {options.map((t) => (
          <option key={t} value={t}>
            {t}
          </option>
        ))}
      </select>
    </div>
  );
}


