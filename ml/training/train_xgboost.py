import os
import pandas as pd
import numpy as np
import joblib
try:
    from xgboost import XGBClassifier
except ImportError:
    print("XGBoost not found. Falling back to GradientBoostingClassifier.")
    from sklearn.ensemble import GradientBoostingClassifier as XGBClassifier
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.metrics import classification_report, accuracy_score

def train_xgboost():
    print("Loading historical data...")
    data_path = "ml/datasets/training/historical_data.csv"
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}. Run data_collector.py first.")
        return

    df = pd.read_csv(data_path, index_col=0)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
    elif df.index.name == 'Date' or isinstance(df.index, pd.DatetimeIndex) or len(str(df.index[0])) > 8:
        # It's likely already a datetime index
        pass

    # Drop target columns from features
    feature_cols = [c for c in df.columns if c not in [
        'Ticker', 'Target_1d_label', 'Target_1w_label', 'Target_1m_label',
        'Return_1d', 'Return_1w', 'Return_1m'
    ]]
    
    # Target label mapping: -1 -> 0, 0 -> 1, 1 -> 2
    # So 0=Bearish, 1=Neutral, 2=Bullish
    X = df[feature_cols].copy()
    y = df['Target_1w_label'].map({-1: 0, 0: 1, 1: 2})

    # Basic time series split
    tscv = TimeSeriesSplit(n_splits=3)
    
    try:
        import xgboost
        xgb = XGBClassifier(objective='multi:softprob', num_class=3, eval_metric='mlogloss', random_state=42)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.05, 0.1],
            'subsample': [0.8, 1.0]
        }
    except ImportError:
        xgb = XGBClassifier(random_state=42)
        param_grid = {
            'n_estimators': [50, 100],
            'max_depth': [3, 5],
            'learning_rate': [0.05, 0.1],
            'subsample': [0.8, 1.0]
        }

    
    print("Running RandomizedSearchCV...")
    search = RandomizedSearchCV(xgb, param_distributions=param_grid, n_iter=5, cv=tscv, scoring='accuracy', n_jobs=-1, random_state=42)
    search.fit(X, y)
    
    best_model = search.best_estimator_
    print(f"Best parameters: {search.best_params_}")
    
    # Feature importance
    importances = best_model.feature_importances_
    feat_imp = pd.Series(importances, index=feature_cols).sort_values(ascending=False)
    print("Top 5 Feature Importances:")
    print(feat_imp.head(5))
    
    # Save the model
    os.makedirs("ml/saved_models", exist_ok=True)
    model_path = "ml/saved_models/xgboost.pkl"
    joblib.dump(best_model, model_path)
    print(f"Model saved to {model_path}")
    
    # Quick eval on last 20% of data
    split_idx = int(len(X) * 0.8)
    X_test, y_test = X.iloc[split_idx:], y.iloc[split_idx:]
    y_pred = best_model.predict(X_test)
    print("Test Accuracy:", accuracy_score(y_test, y_pred))

if __name__ == "__main__":
    train_xgboost()
