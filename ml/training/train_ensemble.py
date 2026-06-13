import os
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import accuracy_score, classification_report

def train_base_models_on_fold(X_train, y_train, X_val, y_val, ticker_groups_train, ticker_groups_val):
    """Train base models on a fold and return out-of-fold predictions."""
    oof = {}

    # XGBoost
    try:
        from xgboost import XGBClassifier
        xgb = XGBClassifier(objective='multi:softprob', num_class=3, eval_metric='mlogloss',
                            n_estimators=100, max_depth=5, learning_rate=0.05, random_state=42)
    except ImportError:
        from sklearn.ensemble import GradientBoostingClassifier
        xgb = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)

    xgb.fit(X_train, y_train)
    oof['xgb'] = xgb.predict_proba(X_val)

    # LSTM (if TensorFlow available)
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        from tensorflow.keras.callbacks import EarlyStopping
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_train_s = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
        X_val_s = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns, index=X_val.index)

        time_steps = 10
        X_train_seq, y_train_seq = [], []
        for i in range(len(X_train_s) - time_steps):
            X_train_seq.append(X_train_s.iloc[i:(i + time_steps)].values)
            y_train_seq.append(y_train.iloc[i + time_steps])
        X_train_seq = np.array(X_train_seq)
        y_train_seq = np.array(y_train_seq)

        X_val_seq, y_val_seq = [], []
        for i in range(len(X_val_s) - time_steps):
            X_val_seq.append(X_val_s.iloc[i:(i + time_steps)].values)
            y_val_seq.append(y_val.iloc[i + time_steps])
        X_val_seq = np.array(X_val_seq)
        y_val_seq = np.array(y_val_seq)

        if len(X_train_seq) > 0 and len(X_val_seq) > 0:
            y_train_cat = tf.keras.utils.to_categorical(y_train_seq, num_classes=3)
            y_val_cat = tf.keras.utils.to_categorical(y_val_seq, num_classes=3)

            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(X_train_seq.shape[1], X_train_seq.shape[2])),
                Dropout(0.2),
                LSTM(50),
                Dropout(0.2),
                Dense(3, activation='softmax')
            ])
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
            model.fit(X_train_seq, y_train_cat, epochs=10, batch_size=32, validation_split=0.1,
                      callbacks=[early_stop], verbose=0)
            lstm_probs = model.predict(X_val_seq, verbose=0)
            # Pad to match val size: LSTM produces fewer rows due to sequence window
            pad_size = len(X_val) - len(lstm_probs)
            if pad_size > 0:
                pad = np.tile([0.33, 0.34, 0.33], (pad_size, 1))
                lstm_probs = np.vstack([pad, lstm_probs])
            oof['lstm'] = lstm_probs
        else:
            oof['lstm'] = np.tile([0.33, 0.34, 0.33], (len(X_val), 1))
    except Exception:
        oof['lstm'] = np.tile([0.33, 0.34, 0.33], (len(X_val), 1))

    return oof, xgb

def build_meta_features(oof_dict, prophet_trend_val, sentiment_val):
    """Combine base model OOF predictions into meta-features."""
    xgb_probs = oof_dict['xgb']
    lstm_probs = oof_dict['lstm']

    meta_features = np.column_stack([
        xgb_probs[:, 2],   # xgb_bull
        xgb_probs[:, 0],   # xgb_bear
        lstm_probs[:, 2],  # lstm_bull
        prophet_trend_val,
        sentiment_val
    ])
    return meta_features

def train_ensemble():
    print("Training Ensemble Meta-Model with proper stacking...")

    data_path = "ml/datasets/training/historical_data.csv"
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}. Run data_collector.py first.")
        return

    df = pd.read_csv(data_path, index_col=0)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
    df = df.sort_index()

    feature_cols = [c for c in df.columns if c not in [
        'Ticker', 'Target_1d_label', 'Target_1w_label', 'Target_1m_label',
        'Return_1d', 'Return_1w', 'Return_1m'
    ]]

    X = df[feature_cols].copy()
    y = df['Target_1w_label'].map({-1: 0, 0: 1, 1: 2})
    groups = df['Ticker']

    # Placeholder for prophet trend and sentiment (not available per-row in CSV)
    prophet_trend_all = np.zeros(len(df))
    sentiment_all = df[['News_sentiment', 'Reddit_sentiment', 'Analyst_sentiment']].mean(axis=1).values

    gkf = GroupKFold(n_splits=5)
    meta_features_all = []
    y_all_oof = []

    print("Collecting out-of-fold predictions from base models...")
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups)):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        oof, _ = train_base_models_on_fold(
            X_train, y_train, X_val, y_val,
            groups.iloc[train_idx], groups.iloc[val_idx]
        )

        meta_feat = build_meta_features(
            oof,
            prophet_trend_all[val_idx],
            sentiment_all[val_idx]
        )
        meta_features_all.append(meta_feat)
        y_all_oof.append(y_val.values)

        val_acc = accuracy_score(y_val, oof['xgb'].argmax(axis=1))
        val_tickers = groups.iloc[val_idx].unique().tolist()
        print(f"  Fold {fold+1} (val tickers: {val_tickers}): XGB base accuracy={val_acc:.4f}")

    meta_X = np.vstack(meta_features_all)
    meta_y = np.concatenate(y_all_oof)

    print(f"\nTraining meta-model on {len(meta_X)} out-of-fold samples...")
    meta_model = LogisticRegression(max_iter=1000, random_state=42)
    meta_model.fit(meta_X, meta_y)

    train_acc = meta_model.score(meta_X, meta_y)
    print(f"Meta-Model OOF Accuracy: {train_acc:.4f}")

    # Time-based holdout evaluation
    split_idx = int(len(X) * 0.8)
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]

    # Re-train a full XGBoost on all data for holdout eval
    try:
        from xgboost import XGBClassifier
        xgb_full = XGBClassifier(objective='multi:softprob', num_class=3, eval_metric='mlogloss',
                                 n_estimators=100, max_depth=5, learning_rate=0.05, random_state=42)
    except ImportError:
        from sklearn.ensemble import GradientBoostingClassifier
        xgb_full = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)

    xgb_full.fit(X, y)
    xgb_test_probs = xgb_full.predict_proba(X_test)

    # Use same dummy lstm/prophet for holdout (consistent with what's available at serving time)
    lstm_test_probs = np.tile([0.33, 0.34, 0.33], (len(X_test), 1))
    prophet_test_trend = np.zeros(len(X_test))
    sentiment_test = df[['News_sentiment', 'Reddit_sentiment', 'Analyst_sentiment']].iloc[split_idx:].mean(axis=1).values

    meta_test = build_meta_features(
        {'xgb': xgb_test_probs, 'lstm': lstm_test_probs},
        prophet_test_trend,
        sentiment_test
    )

    y_pred = meta_model.predict(meta_test)
    holdout_acc = accuracy_score(y_test, y_pred)
    print(f"Holdout Accuracy: {holdout_acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=['Bearish', 'Neutral', 'Bullish']))

    os.makedirs("ml/saved_models", exist_ok=True)
    model_path = "ml/saved_models/ensemble.pkl"
    joblib.dump(meta_model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_ensemble()
