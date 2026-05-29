import os
import pandas as pd
import joblib
from prophet import Prophet
from sklearn.metrics import mean_absolute_error

def train_prophet():
    print("Loading historical data for Prophet...")
    data_path = "ml/datasets/training/historical_data.csv"
    if not os.path.exists(data_path):
        print("Run data_collector.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Prophet requires 'ds' (datetime) and 'y' (target)
    # We will train one generalized model or one per ticker.
    # To keep it simple for the ensemble, we will train a single Prophet model
    # on the most recent data of a representative stock (e.g., AAPL) or just
    # save a template model. Prophet is usually per-ticker.
    # We will train a Prophet model for AAPL and save it as a representative, 
    # but in reality, prediction service should instantiate and predict per-ticker on the fly.
    # Since we need to save a model, we'll fit on the combined dataset's average or just AAPL.
    
    aapl_df = df[df['Ticker'] == 'AAPL'].copy()
    if 'Date' in aapl_df.columns:
        aapl_df['ds'] = pd.to_datetime(aapl_df['Date'], utc=True).dt.tz_localize(None)
    else:
        aapl_df['ds'] = pd.to_datetime(aapl_df.index, utc=True).dt.tz_localize(None)
        
    aapl_df['y'] = aapl_df['Close']
    
    aapl_df = aapl_df[['ds', 'y']].sort_values('ds')
    
    split = int(len(aapl_df) * 0.8)
    train, test = aapl_df.iloc[:split], aapl_df.iloc[split:]
    
    model = Prophet(daily_seasonality=True)
    model.fit(train)
    
    # Eval
    future = model.make_future_dataframe(periods=len(test))
    forecast = model.predict(future)
    y_pred = forecast['yhat'].iloc[split:]
    mae = mean_absolute_error(test['y'], y_pred)
    print(f"Prophet MAE on AAPL test set: {mae:.2f}")
    
    model_path = "ml/saved_models/prophet.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_prophet()
