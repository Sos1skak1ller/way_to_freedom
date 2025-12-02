import React from "react";

export function InfoPanel() {
  return (
    <div>
      <h2>Что здесь происходит</h2>
      <p className="info-text">
        Это простое квант-приложение для бэктеста стратегий на исторических данных.
      </p>

      <h3>Тикеры</h3>
      <p className="info-text">
        В выпадающем списке выбраны популярные инструменты:
      </p>
      <ul className="info-list">
        <li>
          <span className="info-pill">AAPL, MSFT, GOOG</span> — отдельные акции.
        </li>
        <li>
          <span className="info-pill">SPY</span> — ETF на индекс S&amp;P 500.
        </li>
        <li>
          <span className="info-pill">BTC-USD</span> — Bitcoin к доллару.
        </li>
      </ul>

      <h3>Стратегии</h3>
      <ul className="info-list">
        <li>
          <span className="info-pill">MA Crossover</span> — стратегия пересечения скользящих средних.
          <div className="info-small">
            Fast MA &gt; Slow MA — вход в лонг, Fast MA &lt; Slow MA — выход.
          </div>
        </li>
        <li>
          <span className="info-pill">Mean Reversion</span> — возврат к среднему.
          <div className="info-small">
            Покупка при сильном отклонении цены ниже SMA, фиксация, когда цена возвращается выше
            средней.
          </div>
        </li>
        <li>
          <span className="info-pill">Breakout</span> — пробой диапазона.
          <div className="info-small">
            Вход при пробое локального максимума за N дней, выход при уходе ниже локального минимума.
          </div>
        </li>
      </ul>

      <h3>Параметры (ползунки/поля)</h3>
      <ul className="info-list">
        <li>
          <span className="info-pill">Fast / Slow MA</span> — длина "быстрой" и "медленной"
          скользящей средней в днях.
        </li>
        <li>
          <span className="info-pill">Window</span> — размер окна в днях для расчёта среднего,
          волатильности или диапазона.
        </li>
        <li>
          <span className="info-pill">Std K</span> — во сколько стандартных отклонений цена должна
          уйти ниже средней, чтобы считать это "перепроданностью".
        </li>
      </ul>
    </div>
  );
}


