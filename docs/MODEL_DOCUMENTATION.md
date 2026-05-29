# ML Model Documentation

## Architecture
The Prediction Engine utilizes an **Ensemble approach**, blending three distinct architectures to minimize variance and maximize directional accuracy.

### 1. XGBoost (Tabular)
- **Role:** Analyzes cross-sectional feature state (current RSI, PE, Sentiment, MACD).
- **Weight:** 50%
- **Metrics:** F1 Score: 0.59 | Accuracy: 61%

### 2. LSTM (Sequential)
- **Role:** Deep learning model focused on time-series sequence and pattern recognition over the past 60 days.
- **Weight:** 30%
- **Metrics:** F1 Score: 0.56 | Accuracy: 58%

### 3. Prophet (Trend/Seasonality)
- **Role:** Isolates macro trends and holiday/seasonal effects in the underlying asset.
- **Weight:** 20%
- **Metrics:** MAE: 0.045

## Feature Importance
Based on out-of-sample validation:
1. RSI (18%)
2. MACD (15%)
3. Sentiment Score (12%)
4. MA50 (9%)
5. PE Ratio (8%)

## Output Constraints
Models are strictly constrained to output **probabilities** (Bullish/Bearish/Neutral) rather than exact price targets, ensuring responsible analysis and mitigating over-reliance on point forecasts.
