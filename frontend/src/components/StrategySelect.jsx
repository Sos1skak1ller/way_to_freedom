import React from "react";

export function StrategySelect({ value, onChange }) {
  return (
    <div className="field">
      <label
        title={
          "Strategy — торговая логика, по которой генерируются сигналы. " +
          "MA Crossover — пересечение скользящих средних; Mean Reversion — возврат к среднему; " +
          "Breakout — пробой локального диапазона."
        }
      >
        Strategy
      </label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="ma_crossover">MA Crossover</option>
        <option value="mean_reversion">Mean Reversion</option>
        <option value="breakout">Breakout</option>
      </select>
    </div>
  );
}


