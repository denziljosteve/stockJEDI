import os
import pandas as pd
import numpy as np
import joblib
try:
    from xgboost import XGBClassifier
except ImportError:
    print("XGBoost not found. Falling back to GradientBoostingClassifier.")
    from sklearn.ensemble import GradientBoostingClassifier as XGBClassifier
from sklearn.model_selection import GroupKFold, TimeSeriesSplit
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
        pass

    df = df.sort_index()

    # Drop target columns from features
    feature_cols = [c for c in df.columns if c not in [
        'Ticker', 'Target_1d_label', 'Target_1w_label', 'Target_1m_label',
        'Return_1d', 'Return_1w', 'Return_1m'
    ]]
    
    # Target label mapping: -1 -> 0, 0 -> 1, 1 -> 2
    X = df[feature_cols].copy()
    y = df['Target_1w_label'].map({-1: 0, 0: 1, 1: 2})
    groups = df['Ticker']

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

    # GroupKFold by ticker prevents any sample from a ticker appearing
    # in both train and validation, eliminating cross-ticker leakage.
    gkf = GroupKFold(n_splits=5)

    print("Running GroupKFold cross-validation by ticker...")
    scores = []
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups)):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        xgb_clone = XGBClassifier(**xgb.get_params())
        xgb_clone.fit(X_train, y_train)
        y_pred = xgb_clone.predict(X_val)
        score = accuracy_score(y_val, y_pred)
        scores.append(score)
        val_tickers = groups.iloc[val_idx].unique().tolist()
        print(f"  Fold {fold+1} (val tickers: {val_tickers}): accuracy={score:.4f}")

    print(f"Mean CV Accuracy: {np.mean(scores):.4f} (+/- {np.std(scores):.4f})")

    # Final fit on all data for production model
    xgb_final = XGBClassifier(**xgb.get_params())
    xgb_final.fit(X, y)

    # Feature importance
    importances = xgb_final.feature_importances_
    feat_imp = pd.Series(importances, index=feature_cols).sort_values(ascending=False)
    print("Top 5 Feature Importances:")
    print(feat_imp.head(5))
    
    # Save the model
    os.makedirs("ml/saved_models", exist_ok=True)
    model_path = "ml/saved_models/xgboost.pkl"
    joblib.dump(xgb_final, model_path)
    print(f"Model saved to {model_path}")
    
    # Time-based holdout eval: last 20% of chronological data
    split_idx = int(len(X) * 0.8)
    X_test, y_test = X.iloc[split_idx:], y.iloc[split_idx:]
    y_pred = xgb_final.predict(X_test)
    print("Time-based Holdout Accuracy:", accuracy_score(y_test, y_pred))

if __name__ == "__main__":
    train_xgboost()
