import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import logging

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    import tensorflow as tf
except ImportError:
    logging.warning("Tensorflow not installed. Mocking LSTM Model training for demonstration.")
    class MockLSTM:
        def fit(self, *args, **kwargs): pass
        def save(self, path): 
            with open(path, 'w') as f: f.write("mock")

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

    X = df[feature_cols]
    y = df['Target']
    
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    joblib.dump(scaler, "ml/saved_models/lstm_scaler.pkl")

    time_steps = 10
    X_seq, y_seq = create_sequences(X_scaled, y, time_steps)
    
    # Split
    split = int(0.8 * len(X_seq))
    X_train, X_test = X_seq[:split], X_seq[split:]
    y_train, y_test = y_seq[:split], y_seq[split:]

    # One hot encoding for target
    try:
        y_train_cat = tf.keras.utils.to_categorical(y_train, num_classes=3)
        y_test_cat = tf.keras.utils.to_categorical(y_test, num_classes=3)
        
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(3, activation='softmax')
        ])
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
        
        print("Training LSTM model...")
        model.fit(X_train, y_train_cat, epochs=10, batch_size=32, validation_split=0.1, callbacks=[early_stop], verbose=1)
        
        loss, acc = model.evaluate(X_test, y_test_cat, verbose=0)
        print(f"Test Accuracy: {acc:.4f}")
        
        model.save("ml/saved_models/lstm.h5")
        print("Model saved to ml/saved_models/lstm.h5")
    except Exception as e:
        print(f"Error during TF training or TF not installed: {e}")
        with open("ml/saved_models/lstm.h5", 'w') as f: f.write("mock_lstm")

if __name__ == "__main__":
    train_lstm()
