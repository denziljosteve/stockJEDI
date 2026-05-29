# stockJEDI API Documentation

## Base URL
`http://localhost:8000/api/v1`

## Endpoints

### 1. Stock Data
- **GET** `/stock/{ticker}/historical`
  - Retrieves historical OHLCV data.
  - Query Params: `period` (1d, 1w, 1mo, 1y).
- **POST** `/stock/analyze?ticker={ticker}`
  - Triggers data aggregation and technical analysis computation.

### 2. Predictions (ML)
- **POST** `/prediction/{ticker}`
  - Retrieves ensemble probabilities (1-day, 1-week, 1-month).
- **GET** `/prediction/model/metrics`
  - Returns cross-validation and accuracy metrics for the models.

### 3. Sentiment & AI
- **POST** `/sentiment/{ticker}`
  - Fetches news and social data, returning a normalized score (-100 to 100).
- **POST** `/report/{ticker}`
  - Generates the full Groq-powered institutional investment report.

### 4. User Portfolio & Watchlist
- **GET** `/portfolio`
  - Retrieves the authenticated user's portfolio and gain/loss metrics.
- **POST** `/portfolio/add`
  - Adds a transaction (Buy/Sell) to the portfolio.
- **GET** `/watchlist`
  - Retrieves saved tickers.

### 5. Real-Time (WebSockets)
- **WS** `/ws/{ticker}`
  - Connects to the real-time stream for live price and sentiment updates.
