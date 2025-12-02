import React from "react";

export function ParametersForm({ strategy, params, setParams }) {
  const update = (key, value) => {
    setParams((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="params">
      <h3>Parameters</h3>
      {strategy === "ma_crossover" && (
        <div className="params-grid">
          <div className="field">
            <label
              title={
                'Fast / Slow MA — длина "быстрой" и "медленной" скользящей средней в днях. ' +
                'MA Crossover: Fast MA > Slow MA — вход в лонг, Fast MA < Slow MA — выход.'
              }
            >
              Fast MA
            </label>
            <input
              type="number"
              min="2"
              value={params.fast}
              onChange={(e) => update("fast", Number(e.target.value))}
            />
          </div>
          <div className="field">
            <label
              title={
                'Fast / Slow MA — длина "быстрой" и "медленной" скользящей средней в днях. ' +
                "Увеличивайте окно, чтобы сгладить шум, уменьшайте — чтобы получать более частые сигналы."
              }
            >
              Slow MA
            </label>
            <input
              type="number"
              min="3"
              value={params.slow}
              onChange={(e) => update("slow", Number(e.target.value))}
            />
          </div>
        </div>
      )}
      {strategy === "mean_reversion" && (
        <div className="params-grid">
          <div className="field">
            <label
              title={
                "Window — размер окна в днях для расчёта средней цены и волатильности. " +
                "Используется в стратегии Mean Reversion для поиска отклонений от среднего."
              }
            >
              Window
            </label>
            <input
              type="number"
              min="5"
              value={params.window}
              onChange={(e) => update("window", Number(e.target.value))}
            />
          </div>
          <div className="field">
            <label
              title={
                "Std K — во сколько стандартных отклонений цена должна уйти ниже средней, " +
                'чтобы считать это "перепроданностью". Чем больше значение, тем реже сигналы.'
              }
            >
              Std K
            </label>
            <input
              type="number"
              step="0.1"
              value={params.std_k}
              onChange={(e) => update("std_k", Number(e.target.value))}
            />
          </div>
        </div>
      )}
      {strategy === "breakout" && (
        <div className="params-grid">
          <div className="field">
            <label
              title={
                "Window — размер окна в днях для расчёта диапазона High/Low. " +
                "В стратегии Breakout используется для поиска пробоя локального максимума или минимума."
              }
            >
              Window
            </label>
            <input
              type="number"
              min="5"
              value={params.window}
              onChange={(e) => update("window", Number(e.target.value))}
            />
          </div>
        </div>
      )}
    </div>
  );
}


