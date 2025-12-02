## Quant Backtester MVP

**Backend**: FastAPI + Python  
**Frontend**: React + Vite  
**Data**: `yfinance` (акции), `ccxt` (крипта), кэш в Parquet.

### Функциональность

- **Загрузка данных**: OHLCV из `yfinance`/`ccxt` с Parquet-кэшем.
- **Стратегии**:
  - MA Crossover (MA20/MA50 по умолчанию, параметры настраиваются)
  - Mean Reversion (SMA ± k·std)
  - Breakout (пробой max/high, min/low за N дней)
- **Бэктестинг**:
  - симуляция сделок и equity curve
  - метрики: Sharpe, Sortino, Max Drawdown, CAGR, Volatility, Win Rate, Profit Factor
- **API**:
  - `POST /data/load` — загрузка и кэширование исторических данных
  - `POST /backtest/run` — запуск бэктеста, возврат equity, цен, сигналов, метрик и списка сделок
- **Frontend**:
  - форма выбора тикера/стратегии/параметров/периода
  - график equity
  - график цены + сигналы
  - таблица сделок

### Структура проекта

```text
/backend
  main.py
  requirements.txt
  /api
    data_api.py
    backtest_api.py
  /data
    fetch.py
  /strategies
    ma_crossover.py
    mean_reversion.py
    breakout.py
  /backtest
    engine.py
    metrics.py
  /utils
    plot.py

/frontend
  package.json
  vite.config.mjs
  index.html
  /src
    main.jsx
    App.jsx
    styles.css
    /components
      TickerSelect.jsx
      StrategySelect.jsx
      ParametersForm.jsx
      BacktestButton.jsx
      EquityChart.jsx
      PriceChart.jsx
      TradesTable.jsx
```

### Запуск через Docker

В корне проекта:

```bash
docker compose up --build
```

После этого:

- backend будет доступен на `http://localhost:8000`
- frontend (React+Vite) — на `http://localhost:5173`

Фронтенд внутри контейнера по-прежнему ходит на `http://localhost:8000/backtest/run`, так как backend проброшен на хост.

### Запуск backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Интерактивная документация API (Swagger UI) будет доступна по адресу:

- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc

### Запуск frontend

```bash
cd frontend
npm install
npm run dev
```

Фронтенд ожидает backend по адресу `http://localhost:8000`.


### Пример запроса к API бэктеста

```bash
curl -X POST http://localhost:8000/backtest/run \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "strategy": "ma_crossover",
    "params": { "fast": 20, "slow": 50 },
    "period": { "start": "2018-01-01", "end": "2024-01-01" },
    "source": "yfinance",
    "interval": "1d",
    "initial_capital": 10000
  }'
```


