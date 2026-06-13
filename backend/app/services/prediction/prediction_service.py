import sys
import os
import numpy as np
from typing import Dict, Any, List
from loguru import logger

# Ensure the ml package is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from ml.models.ensemble_model import ensemble_model

class PredictionService:
    _models_loaded = False
    _model_cache = {
        'xgb': None,
        'lstm': None,
        'prophet': None,
        'meta': None
    }

    @classmethod
    def _ensure_models_loaded(cls):
        if not cls._models_loaded:
            try:
                ensemble_model.xgb.load_model()
                ensemble_model.lstm.load_model()
                ensemble_model.prophet.load_model()
                ensemble_model.load_meta_model()
                cls._models_loaded = True
                logger.info("Prediction models loaded successfully")
            except Exception as e:
                logger.error(f"Error loading prediction models: {e}")
                raise

    @classmethod
    def refresh_models(cls):
        cls._models_loaded = False
        cls._ensure_models_loaded()

    @staticmethod
    def get_predictions(ticker: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate probability-based predictions for multiple horizons.
        """
        PredictionService._ensure_models_loaded()

        info = market_data.get('info', {})
        inds = market_data.get('indicators', {})

        sentiment_score = 0.0

        current_price = info.get('current_price', 0.0)

        feature_dict = {
            'Open': info.get('open', current_price),
            'High': info.get('high', current_price),
            'Low': info.get('low', current_price),
            'Close': current_price,
            'Volume': info.get('volume', 0),
            'RSI': inds.get('rsi', 50.0) or 50.0,
            'MACD': inds.get('macd', 0.0) or 0.0,
            'MA20': inds.get('ma20', current_price) or current_price,
            'MA50': inds.get('ma50', current_price) or current_price,
            'MA100': inds.get('ma100', current_price) or current_price,
            'MA200': inds.get('ma200', current_price) or current_price,
            'ATR': inds.get('atr', 0.0) or 0.0,
            'VWAP': inds.get('vwap', current_price) or current_price,
            'ADX': inds.get('adx', 20.0) or 20.0,
            'PE': info.get('pe_ratio', 15.0) or 15.0,
            'EPS': info.get('eps', 5.0) or 5.0,
            'Revenue_growth': info.get('revenue_growth', 0.05) or 0.05,
            'ROE': info.get('roe', 0.1) or 0.1,
            'Debt_Equity': info.get('debt_to_equity', 50.0) or 50.0,
            'News_sentiment': 0.0,
            'Reddit_sentiment': 0.0,
            'Analyst_sentiment': 0.0
        }

        import pandas as pd
        features_df = pd.DataFrame([feature_dict])

        pred_1d = ensemble_model.predict_probabilities(features_df, horizon_days=1, current_price=current_price, sentiment_score=sentiment_score)
        pred_1w = ensemble_model.predict_probabilities(features_df, horizon_days=7, current_price=current_price, sentiment_score=sentiment_score)
        pred_1m = ensemble_model.predict_probabilities(features_df, horizon_days=30, current_price=current_price, sentiment_score=sentiment_score)

        confidence = "Medium"
        if pred_1w['bullish'] > 65 or pred_1w['bearish'] > 65:
            confidence = "High"
        elif 40 < pred_1w['bullish'] < 60 and 40 < pred_1w['bearish'] < 60:
            confidence = "Low"

        signals = PredictionService._generate_signals(market_data, pred_1w)

        return {
            "ticker": ticker,
            "1_day": pred_1d,
            "1_week": pred_1w,
            "1_month": pred_1m,
            "confidence": confidence,
            "signals": signals
        }

    @staticmethod
    def _generate_signals(market_data: Dict[str, Any], pred: Dict[str, float]) -> List[str]:
        signals = []
        indicators = market_data.get('indicators', {})

        if indicators.get('trend') == 'Bullish':
            signals.append("Moving averages indicate a strong uptrend.")
        elif indicators.get('trend') == 'Bearish':
            signals.append("Moving averages indicate a strong downtrend.")

        rsi = indicators.get('rsi', 50)
        if rsi > 70:
            signals.append("RSI suggests the asset is currently overbought.")
        elif rsi < 30:
            signals.append("RSI suggests the asset is currently oversold.")

        if pred['bullish'] > pred['bearish']:
            signals.append("Ensemble model leans bullish based on combined feature analysis.")
        else:
            signals.append("Ensemble model leans bearish based on combined feature analysis.")

        return signals

prediction_service = PredictionService()
