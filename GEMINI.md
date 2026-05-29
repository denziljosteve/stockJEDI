# stockJEDI — Gemini.md

## Project Name

stockJEDI

Tagline:

"AI-Powered Stock Intelligence and Investment Analysis Platform"

---

# Project Overview

stockJEDI is an AI-powered stock intelligence platform that accepts stock URLs, ticker symbols, or company names from financial platforms and produces institutional-style investment analysis.

The application gathers market data, performs technical and fundamental analysis, applies prediction models, generates probabilistic movement forecasts, and uses a Groq LLM to create detailed investor-grade reports.

The system must provide:

* Fundamental analysis
* Technical analysis
* Sentiment analysis
* Risk assessment
* Valuation analysis
* Competitor comparison
* Probability-based stock movement forecasting
* Buy/Sell/Hold recommendation
* Investment score
* Confidence score
* Explainable AI reasoning

---

# Supported Input Sources

Supported URL sources:

* Yahoo Finance
* Screener.in
* TradingView
* NSE
* BSE
* Moneycontrol
* MarketWatch
* Alpha Vantage
* Public finance data sources

Supported inputs:

Stock URL:

https://finance.yahoo.com/quote/AAPL

Ticker:

AAPL

Company name:

Apple Inc

---

# Main User Flow

User Input

↓

URL/Ticker Validation

↓

Ticker Extraction

↓

Data Collection Layer

↓

Data Normalization

↓

Technical Analysis

↓

Sentiment Analysis

↓

Prediction Engine

↓

Groq Analysis Layer

↓

Scoring Engine

↓

Dashboard + AI Report

---

# System Architecture

Frontend:

Next.js

React

TailwindCSS

TypeScript

Charts:

TradingView widgets

Chart.js

Recharts

Backend:

FastAPI

Python

Prediction Layer:

XGBoost

LSTM

Prophet

Ensemble Model

AI Layer:

Groq API

Recommended models:

Fast analysis:

llama-3.3-70b-versatile

Deep reasoning:

deepseek-r1-distill-llama

Database:

PostgreSQL

Caching:

Redis

Background Jobs:

Celery

Deployment:

Docker

---

# Folder Structure

stockJEDI/

├── frontend/

├── backend/

├── ml/

├── prompts/

├── jobs/

├── database/

├── docs/

├── deployment/

├── monitoring/

├── logs/

├── README.md

├── .env

├── docker-compose.yml

└── gemini.md

---

# Module 1: URL Processing Engine

Purpose:

Accept stock links and extract ticker information.

Tasks:

1. Validate URL

2. Detect provider

3. Extract ticker

4. Verify company information

Example:

Input:

https://finance.yahoo.com/quote/TSLA

Output:

Ticker:

TSLA

Source:

Yahoo Finance

---

# Module 2: Data Aggregation Engine

Collect:

Price Data:

* Open
* Close
* High
* Low
* Volume

Historical Data:

* 1 Day
* 1 Week
* 1 Month
* 3 Months
* 6 Months
* 1 Year
* 5 Years

Financial Statements:

Income Statement

Balance Sheet

Cash Flow Statement

Financial Metrics:

* PE Ratio
* PEG Ratio
* EPS
* Revenue Growth
* ROE
* ROA
* Debt-to-equity
* Free Cash Flow
* Profit Margin

---

# Module 3: Technical Analysis Engine

Indicators:

* RSI
* MACD
* Moving Averages
* Bollinger Bands
* VWAP
* ATR
* Stochastic RSI
* ADX

Pattern Detection:

* Head and Shoulders
* Double Top
* Double Bottom
* Triangle
* Breakout
* Flag
* Wedge

Trend Analysis:

* Support Levels
* Resistance Levels
* Trend Strength

---

# Module 4: Sentiment Engine

Analyze:

News

Financial articles

Reddit discussions

Social media posts

Analyst commentary

Output:

Positive score

Negative score

Neutral score

Overall sentiment score

Example:

Sentiment Score: 

74/100

---

# Module 5: Prediction Engine

Purpose:

Estimate likely stock movement scenarios.

Models:

XGBoost

LSTM

Prophet

Ensemble Model

Input Features:

Price data

Volume

Technical indicators

Sentiment

Financial ratios

Sector performance

Market conditions

Prediction Horizons:

1 Day

1 Week

1 Month

3 Months

6 Months

1 Year

Example Output:

1 Week:

Bullish:

62%

Bearish:

24%

Neutral:

14%

Confidence:

Medium

---

# Ensemble Logic

Weighted prediction:

XGBoost:

40%

LSTM:

25%

Sentiment:

20%

Prophet:

10%

Technical Rules:

5%

Final Output:

Bullish Probability

Bearish Probability

Neutral Probability

Confidence Score

---

# Module 6: AI Analysis Layer

Input:

Structured JSON:

{

company:{},

financials:{},

technicalIndicators:{},

sentiment:{},

predictions:{},

sectorData:{}

}

Prompt:

You are an expert institutional equity analyst.

Analyze the stock comprehensively and provide:

1. Company overview

2. Financial health

3. Technical analysis

4. Growth outlook

5. Strengths

6. Weaknesses

7. Risks

8. Competitor comparison

9. Market sentiment

10. Investment thesis

11. Buy/Sell/Hold recommendation

12. Confidence level

13. Investment score

14. Risk explanation

15. Bullish/Bearish probabilities

---

# Investment Scoring Engine

Weight Distribution:

Fundamentals:

35%

Technical:

25%

Sentiment:

15%

Growth:

15%

Risk:

10%

Formula:

Overall Score =

(Fundamental × .35)

*

(Technical × .25)

*

(Sentiment × .15)

*

(Growth × .15)

*

(Risk × .10)

Score Interpretation:

0–30

Very Weak

31–50

Weak

51–70

Average

71–85

Strong

86–100

Exceptional

---

# Recommendation Rules

Score >80

Bullish >70%

Risk <30

Recommendation:

Strong Buy

---

Score 65–80

Recommendation:

Buy

---

Score 45–65

Recommendation:

Hold

---

Score 30–45

Recommendation:

Sell

---

Score <30

Recommendation:

Strong Sell

---

# Dashboard Design

Top Area:

Company logo

Ticker

Current price

Daily movement

Market cap

Overall score

Recommendation badge

Main Sections:

Overview

Technical Analysis

Fundamental Analysis

Prediction

Sentiment

Risk Analysis

AI Report

Competitors

News

Charts:

Candlestick chart

Prediction chart

Volume chart

Technical indicators

Support/resistance chart

---

# Security Requirements

Use environment variables

Hide API keys

Input validation

Rate limiting

Authentication

Request sanitization

Caching

Secure database connections

---

# Future Features

Portfolio management

AI stock screener

Watchlists

Options analysis

Dividend forecasting

Real-time alerts

Voice assistant

Institutional ownership tracking

AI investment chatbot

Backtesting engine

---

# Constraints

Never claim guaranteed stock prediction

Always show confidence levels

Always explain recommendations

Always show risk warnings

Always display source attribution

Always provide probability-based forecasts

---

# Success Metrics

Average response time:

<5 seconds

Prediction confidence calibration:

Continuously monitored

API uptime:

99.9%

User satisfaction target:

> 90%

---

End of stockJEDI Gemini.md
