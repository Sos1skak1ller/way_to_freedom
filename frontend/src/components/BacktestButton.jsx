import React from "react";

export function BacktestButton({ onClick, loading }) {
  return (
    <button className="primary-btn" onClick={onClick} disabled={loading}>
      {loading ? "Running..." : "Run Backtest"}
    </button>
  );
}


