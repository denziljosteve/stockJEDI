import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.metrics import accuracy_score
import logging

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    import tensorflow as tf
except ImportError:
    logging.warning("Tensorflow not installed. Mocking LSTM Model training for demonstration.")
    tf = None

def create_sequences(X, y, time_steps=10):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X.iloc[i:(i + time_steps)].values)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

def train_lstm():
    print("Loading historical data for LSTM...")
    data_path = "ml/datasets/training/historical_data.csv"
    if not os.path.exists(data_path):
        print("Run data_collector.py first.")
        return

    df = pd.read_csv(data_path, index_col=0)
    
    feature_cols = [c for c in df.columns if c not in [
        'Ticker', 'Target_1d_label', 'Target_1w_label', 'Target_1m_label',
        'Return_1d', 'Return_1w', 'Return_1m'
    ]]
    
    # 0=Bearish, 1=Neutral, 2=Bullish
    df['Target'] = df['Target_1w_label'].map({-1: 0, 0: 1, 1: 2})
    df = df.dropna()
    df = df.sort_index()

    # GroupKFold by ticker prevents cross-ticker data leakage.
    # Samples within each fold come from tickers unseen during training.
    gkf = GroupKFold(n_splits=5)

    all_indices = np.arange(len(df))
    groups = df['Ticker'].values

    scaler = StandardScaler()
    X_all = df[feature_cols]
    y_all = df['Target']
    X_scaled_full = pd.DataFrame(scaler.fit_transform(X_all), columns=X_all.columns, index=X_all.index)

    time_steps = 10

    if tf is None:
        print("TensorFlow not available. Skipping LSTM training.")
        os.makedirs("ml/saved_models", exist_ok=True)
        joblib.dump(scaler, "ml/saved_models/lstm_scaler.pkl")
        return

    scores = []
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X_scaled_full, y_all, groups)):
        X_train_fold = X_scaled_full.iloc[train_idx]
        y_train_fold = y_all.iloc[train_idx]
        X_val_fold = X_scaled_full.iloc[val_idx]
        y_val_fold = y_all.iloc[val_idx]

        X_train_seq, y_train_seq = create_sequences(X_train_fold, y_train_fold, time_steps)
        X_val_seq, y_val_seq = create_sequences(X_val_fold, y_val_fold, time_steps)

        if len(X_train_seq) == 0 or len(X_val_seq) == 0:
            continue

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

        _, acc = model.evaluate(X_val_seq, y_val_cat, verbose=0)
        val_tickers = groups[val_idx].unique().tolist()
        print(f"  Fold {fold+1} (val tickers: {val_tickers}): accuracy={acc:.4f}")
        scores.append(acc)

    if scores:
        print(f"Mean CV Accuracy: {np.mean(scores):.4f} (+/- {np.std(scores):.4f})")

    # Final model on all data
    X_seq_all, y_seq_all = create_sequences(X_scaled_full, y_all, time_steps)
    y_cat_all = tf.keras.utils.to_categorical(y_seq_all, num_classes=3)

    final_model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X_seq_all.shape[1], X_seq_all.shape[2])),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(3, activation='softmax')
    ])
    final_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    final_model.fit(X_seq_all, y_cat_all, epochs=10, batch_size=32, verbose=0)

    os.makedirs("ml/saved_models", exist_ok=True)
    joblib.dump(scaler, "ml/saved_models/lstm_scaler.pkl")
    final_model.save("ml/saved_models/lstm.h5")
    print("Models saved to ml/saved_models/")

    # Time-based holdout
    split = int(0.8 * len(X_seq_all))
    X_test, y_test = X_seq_all[split:], y_seq_all[split:]
    y_test_cat = tf.keras.utils.to_categorical(y_test, num_classes=3)
    loss, acc = final_model.evaluate(X_test, y_test_cat, verbose=0)
    print(f"Time-based Holdout Accuracy: {acc:.4f}")

if __name__ == "__main__":
    train_lstm()
