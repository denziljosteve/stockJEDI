export interface MarketData {
  ticker: string;
  company_name: string;
  current_price: number;
  market_cap: number;
  volume: number;
  pe_ratio: number;
  eps: number;
  sector: string;
}

export interface TechnicalIndicators {
  rsi: number;
  macd: number;
  macd_signal: number;
  trend: "Bullish" | "Bearish" | "Neutral";
  signals: string[];
}

export interface SentimentResult {
  overall_sentiment: number;
  positive_score: number;
  negative_score: number;
  neutral_score: number;
  confidence: number;
  summary: string;
}

export interface PredictionResult {
  ticker: string;
  "1_day": { bullish: number; bearish: number; neutral: number };
  "1_week": { bullish: number; bearish: number; neutral: number };
  "1_month": { bullish: number; bearish: number; neutral: number };
  confidence: string;
  signals: string[];
}

export interface AIReport {
  company: MarketData;
  technicalIndicators: TechnicalIndicators;
  sentiment: SentimentResult;
  scoring: {
    overall_score: number;
    recommendation: string;
    confidence: string;
    breakdown: any;
  };
  report_content: string;
}
