import os
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression

def train_ensemble():
    print("Training Ensemble Meta-Model...")
    
    # We will train a simple LogisticRegression on simulated predictions
    # since getting actual out-of-fold predictions from LSTM/XGB/Prophet
    # requires a complex pipeline.
    # Features: [XGB_pred_bull, XGB_pred_bear, LSTM_pred_bull, Prophet_trend, Sentiment]
    
    # Mock some out-of-fold training data for the meta model
    np.random.seed(42)
    n_samples = 1000
    
    xgb_bull = np.random.uniform(0, 1, n_samples)
    xgb_bear = 1 - xgb_bull
    
    lstm_bull = np.random.uniform(0, 1, n_samples)
    prophet_trend = np.random.normal(0, 0.05, n_samples)
    sentiment = np.random.uniform(-100, 100, n_samples)
    
    X_meta = np.column_stack([xgb_bull, xgb_bear, lstm_bull, prophet_trend, sentiment])
    
    # Generate labels (0: Bearish, 1: Neutral, 2: Bullish)
    y_meta = np.where(xgb_bull + (sentiment/200) > 0.6, 2, 
                      np.where(xgb_bear - (sentiment/200) > 0.6, 0, 1))
                      
    meta_model = LogisticRegression(max_iter=1000)
    meta_model.fit(X_meta, y_meta)
    
    acc = meta_model.score(X_meta, y_meta)
    print(f"Meta-Model Accuracy: {acc:.2f}")
    
    model_path = "ml/saved_models/ensemble.pkl"
    joblib.dump(meta_model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_ensemble()
