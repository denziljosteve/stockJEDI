import os
import pandas as pd
import joblib
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import warnings

def train_prophet():
    print("Loading historical data for Prophet...")
    data_path = "ml/datasets/training/historical_data.csv"
    if not os.path.exists(data_path):
        print("Run data_collector.py first.")
        return

    df = pd.read_csv(data_path)

    tickers = df['Ticker'].unique()
    print(f"Prophet: training on {len(tickers)} tickers: {', '.join(tickers)}")

    models = {}
    for ticker in tickers:
        tdf = df[df['Ticker'] == ticker].copy()
        if 'Date' in tdf.columns:
            tdf['ds'] = pd.to_datetime(tdf['Date'], utc=True).dt.tz_localize(None)
        else:
            tdf['ds'] = pd.to_datetime(tdf.index, utc=True).dt.tz_localize(None)

        tdf['y'] = tdf['Close']
        tdf = tdf[['ds', 'y']].sort_values('ds')

        if len(tdf) < 50:
            print(f"  Skipping {ticker}: insufficient data ({len(tdf)} rows)")
            continue

        split = int(len(tdf) * 0.8)
        train, test = tdf.iloc[:split], tdf.iloc[split:]

        model = Prophet(daily_seasonality=True)
        model.fit(train)

        future = model.make_future_dataframe(periods=len(test))
        forecast = model.predict(future)
        y_pred = forecast['yhat'].iloc[split:]
        mae = mean_absolute_error(test['y'], y_pred)
        print(f"  {ticker} MAE on test set: {mae:.2f}")

        models[ticker] = model

    if not models:
        print("WARNING: No Prophet models were trained. All tickers had insufficient data.")
        return

    if len(models) < len(tickers):
        warnings.warn(
            f"Prophet was only trained on {len(models)}/{len(tickers)} tickers. "
            f"Ensemble predictions for untrained tickers will fall back to the default."
        )

    os.makedirs("ml/saved_models", exist_ok=True)
    model_path = "ml/saved_models/prophet.pkl"
    joblib.dump(models, model_path)
    print(f"Models saved to {model_path}")

if __name__ == "__main__":
    train_prophet()
