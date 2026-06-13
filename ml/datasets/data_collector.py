import os
import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, ADXIndicator, SMAIndicator
from ta.volatility import AverageTrueRange

def get_historical_data(ticker, period="5y"):
    print(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    if df.empty:
        return None
        
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    
    # Calculate Technicals
    df['RSI'] = RSIIndicator(close=df['Close'], window=14).rsi()
    macd_obj = MACD(close=df['Close'])
    df['MACD'] = macd_obj.macd()
    df['MA20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
    df['MA50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['MA100'] = SMAIndicator(close=df['Close'], window=100).sma_indicator()
    df['MA200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
    df['ATR'] = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14).average_true_range()
    
    # VWAP approximation (assuming typical price * volume over rolling window or cumulative for the day, but we only have daily data)
    # So we'll calculate a rolling 20-day VWAP
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    df['VWAP'] = (typical_price * df['Volume']).rolling(20).sum() / df['Volume'].rolling(20).sum()
    
    df['ADX'] = ADXIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=14).adx()
    
    # Static Fundamentals (mocked over time as yfinance historical financials are hard to pull at scale without paid APIs)
    try:
        info = stock.info
        df['PE'] = info.get('forwardPE', 15.0)
        df['EPS'] = info.get('trailingEps', 5.0)
        df['Revenue_growth'] = info.get('revenueGrowth', 0.05)
        df['ROE'] = info.get('returnOnEquity', 0.1)
        df['Debt_Equity'] = info.get('debtToEquity', 50.0)
    except:
        df['PE'] = 15.0
        df['EPS'] = 5.0
        df['Revenue_growth'] = 0.05
        df['ROE'] = 0.1
        df['Debt_Equity'] = 50.0

    # Sentiment features: placeholder columns with neutral defaults.
    # Random noise was removed to prevent training on meaningless correlations.
    # Replace with real sentiment data (e.g., FinBERT, VADER, or an external API)
    # when a sentiment source is integrated.
    df['News_sentiment'] = 0.0
    df['Reddit_sentiment'] = 0.0
    df['Analyst_sentiment'] = 0.0
    
    # Target Variables (Future Returns)
    df['Return_1d'] = df['Close'].shift(-1) / df['Close'] - 1
    df['Return_1w'] = df['Close'].shift(-5) / df['Close'] - 1
    df['Return_1m'] = df['Close'].shift(-20) / df['Close'] - 1
    
    # Labeling logic: > 2% is Bullish, < -2% is Bearish, else Neutral (for 1w)
    def label_return(ret, threshold=0.015):
        if pd.isna(ret): return np.nan
        if ret > threshold: return 1  # Bullish
        elif ret < -threshold: return -1 # Bearish
        else: return 0 # Neutral
        
    df['Target_1d_label'] = df['Return_1d'].apply(lambda x: label_return(x, 0.005))
    df['Target_1w_label'] = df['Return_1w'].apply(lambda x: label_return(x, 0.015))
    df['Target_1m_label'] = df['Return_1m'].apply(lambda x: label_return(x, 0.04))

    df = df.dropna()
    df['Ticker'] = ticker
    return df

def collect_data():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "JNJ"]
    all_data = []
    
    os.makedirs("ml/datasets/training", exist_ok=True)
    
    for t in tickers:
        df = get_historical_data(t)
        if df is not None:
            all_data.append(df)
            
    if all_data:
        final_df = pd.concat(all_data)
        output_path = "ml/datasets/training/historical_data.csv"
        final_df.to_csv(output_path)
        print(f"Saved {len(final_df)} rows to {output_path}")

if __name__ == "__main__":
    collect_data()
