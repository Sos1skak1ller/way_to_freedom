import React, { useEffect, useState } from "react";
import { TickerSelect } from "./components/TickerSelect.jsx";
import { StrategySelect } from "./components/StrategySelect.jsx";
import { ParametersForm } from "./components/ParametersForm.jsx";
import { BacktestButton } from "./components/BacktestButton.jsx";
import { EquityChart } from "./components/EquityChart.jsx";
import { PriceChart } from "./components/PriceChart.jsx";
import { TradesTable } from "./components/TradesTable.jsx";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [strategy, setStrategy] = useState("ma_crossover");
  const [params, setParams] = useState({ fast: 20, slow: 50, window: 20, std_k: 2.0 });
  const [start, setStart] = useState("2018-01-01");
  const [end, setEnd] = useState("2024-01-01");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [equity, setEquity] = useState([]);
  const [labels, setLabels] = useState([]);
  const [price, setPrice] = useState([]);
  const [signals, setSignals] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [trades, setTrades] = useState([]);

  const [theme, setTheme] = useState("light");

  useEffect(() => {
    document.body.classList.remove("theme-light", "theme-dark");
    document.body.classList.add(`theme-${theme}`);
  }, [theme]);

  const handleRun = async () => {
    setLoading(true);
    setError(null);

    const body = {
      ticker,
      strategy,
      params:
        strategy === "ma_crossover"
          ? { fast: params.fast, slow: params.slow }
          : strategy === "mean_reversion"
          ? { window: params.window, std_k: params.std_k }
          : { window: params.window },
      period: { start, end },
      source: "yfinance",
      interval: "1d",
      initial_capital: 10000
    };

    try {
      const res = await fetch(`${API_BASE}/backtest/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setEquity(data.equity || []);
      setLabels(data.labels || []);
      setPrice(data.price || []);
      setSignals(data.signals || []);
      setMetrics(data.metrics || null);
      setTrades(data.trades || []);
    } catch (e) {
      console.error(e);
      setError(e.message || "Error");
    } finally {
      setLoading(false);
    }
  };

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  const metricsConfig = [
    { key: "sharpe", label: "Sharpe", isPercent: false },
    { key: "sortino", label: "Sortino", isPercent: false },
    { key: "max_drawdown", label: "Max DD", isPercent: true },
    { key: "cagr", label: "CAGR", isPercent: true },
    { key: "volatility", label: "Volatility", isPercent: true },
    { key: "win_rate", label: "Win Rate", isPercent: true },
    { key: "profit_factor", label: "Profit Factor", isPercent: false }
  ];

  return (
    <div className={`app theme-${theme}`}>
      <header className="header">
        <h1>Quant Backtester MVP</h1>
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "light" ? "Dark mode" : "Light mode"}
        </button>
      </header>

      <section className="controls">
        <div className="controls-row">
          <TickerSelect value={ticker} onChange={setTicker} />
          <StrategySelect value={strategy} onChange={setStrategy} />
        </div>
        <div className="controls-row">
          <div className="field">
            <label>Start</label>
            <input type="date" value={start} onChange={(e) => setStart(e.target.value)} />
          </div>
          <div className="field">
            <label>End</label>
            <input type="date" value={end} onChange={(e) => setEnd(e.target.value)} />
          </div>
        </div>
        <ParametersForm strategy={strategy} params={params} setParams={setParams} />
        <BacktestButton onClick={handleRun} loading={loading} />
        {error && <div className="error">Ошибка: {error}</div>}
      </section>

      <section className="charts">
        <div className="chart-card">
          <h2>Equity Curve</h2>
          <EquityChart equity={equity} labels={labels} theme={theme} />
        </div>
        <div className="chart-card">
          <h2>Price & Signals</h2>
          <PriceChart price={price} labels={labels} signals={signals} theme={theme} />
        </div>
      </section>

      <section className="metrics-trades">
        <div className="metrics-card">
          <h2>Metrics</h2>
          {metrics ? (
            <ul>
              {metricsConfig.map((m) => {
                const value = metrics[m.key];
                let display;
                if (value == null) {
                  display = "—";
                } else if (m.isPercent) {
                  display = `${(value * 100).toFixed(2)}%`;
                } else {
                  display = value.toFixed(2);
                }

                let cls = "metric-neutral";
                if (value != null) {
                  if (value > 0) cls = "metric-positive";
                  else if (value < 0) cls = "metric-negative";
                }

                return (
                  <li key={m.key} className={cls}>
                    <span>{m.label}</span>
                    <span>{display}</span>
                  </li>
                );
              })}
            </ul>
          ) : (
            <div className="placeholder">Запустите бэктест, чтобы увидеть метрики</div>
          )}
        </div>
        <div className="trades-card">
          <h2>Trades</h2>
          <TradesTable trades={trades} />
        </div>
      </section>
    </div>
  );
}


