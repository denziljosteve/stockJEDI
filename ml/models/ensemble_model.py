import os
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any

class XGBoostModel:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        try:
            self.model = joblib.load("ml/saved_models/xgboost.pkl")
        except:
            self.model = None

    def predict_proba(self, features: pd.DataFrame) -> np.ndarray:
        if self.model is None:
            return np.array([[0.33, 0.33, 0.34]])
        # xgboost multi:softprob outputs probabilities for each class
        # order is based on label mapping: 0=Bearish, 1=Neutral, 2=Bullish
        return self.model.predict_proba(features)
        
class LSTMModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
        
    def load_model(self):
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model("ml/saved_models/lstm.h5")
            self.scaler = joblib.load("ml/saved_models/lstm_scaler.pkl")
        except:
            self.model = None

    def predict_proba(self, features: pd.DataFrame) -> np.ndarray:
        if self.model is None or self.scaler is None:
            return np.array([[0.33, 0.33, 0.34]])
        
        # Need sequences of length 10. If we only have 1 row, we just duplicate it or pad.
        # In a real scenario, PredictionService should fetch the last 10 days of data.
        # For this prototype to run on 1 row, we'll repeat the row 10 times to form a sequence.
        # This is a hack for the demonstration to ensure dimensionality matches.
        X_scaled = self.scaler.transform(features)
        seq = np.tile(X_scaled[0], (10, 1)).reshape(1, 10, -1)
        
        pred = self.model.predict(seq, verbose=0)
        return pred

class ProphetModel:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        try:
            self.model = joblib.load("ml/saved_models/prophet.pkl")
        except:
            self.model = None

    def predict_trend(self, current_price: float, days: int) -> float:
        if self.model is None:
            return 0.0
        
        future = self.model.make_future_dataframe(periods=days)
        forecast = self.model.predict(future)
        pred_price = forecast['yhat'].iloc[-1]
        
        return (pred_price - current_price) / current_price

class EnsembleModel:
    def __init__(self):
        self.xgb = XGBoostModel()
        self.lstm = LSTMModel()
        self.prophet = ProphetModel()
        self.meta_model = None
        self.load_meta_model()
        
    def load_meta_model(self):
        try:
            self.meta_model = joblib.load("ml/saved_models/ensemble.pkl")
        except:
            self.meta_model = None
        
    def predict_probabilities(self, features: pd.DataFrame, horizon_days: int, current_price: float, sentiment_score: float) -> Dict[str, float]:
        """
        Returns a probability distribution for Bullish, Bearish, and Neutral movements.
        """
        # Ensure correct column order for XGB and LSTM based on training
        # We assume `features` is a DataFrame with the correct columns from the pipeline.
        
        # 1. XGBoost Predict (0=Bearish, 1=Neutral, 2=Bullish)
        xgb_probs = self.xgb.predict_proba(features)[0]
        xgb_bear = xgb_probs[0]
        xgb_bull = xgb_probs[2]
        
        # 2. LSTM Predict
        lstm_probs = self.lstm.predict_proba(features)[0]
        lstm_bull = lstm_probs[2]
        
        # 3. Prophet Trend
        prophet_trend = self.prophet.predict_trend(current_price, horizon_days)
        
        # 4. Use Meta Model if available
        if self.meta_model is not None:
            # Features: [XGB_pred_bull, XGB_pred_bear, LSTM_pred_bull, Prophet_trend, Sentiment]
            meta_features = np.array([[xgb_bull, xgb_bear, lstm_bull, prophet_trend, sentiment_score]])
            meta_probs = self.meta_model.predict_proba(meta_features)[0]
            # Meta labels: 0=Bearish, 1=Neutral, 2=Bullish
            bearish = meta_probs[0] * 100
            neutral = meta_probs[1] * 100
            bullish = meta_probs[2] * 100
        else:
            # Fallback simple weighting if meta model fails
            bullish = (xgb_bull * 0.5 + lstm_bull * 0.3 + (prophet_trend > 0) * 0.2) * 100
            bearish = (xgb_bear * 0.5 + (1-lstm_bull) * 0.3 + (prophet_trend < 0) * 0.2) * 100
            neutral = max(0, 100 - bullish - bearish)

        # Normalize to 100% just in case
        total = bullish + bearish + neutral
        if total > 0:
            bullish = (bullish / total) * 100
            bearish = (bearish / total) * 100
            neutral = (neutral / total) * 100
            
        return {
            "bullish": round(bullish, 1),
            "bearish": round(bearish, 1),
            "neutral": round(neutral, 1)
        }

ensemble_model = EnsembleModel()
