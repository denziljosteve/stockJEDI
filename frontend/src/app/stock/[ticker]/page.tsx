'use client';
import { useQuery } from '@tanstack/react-query';
import { predictionService, reportService } from '@/services/api';
import RecommendationCard from '@/components/cards/RecommendationCard';
import { StockPageSkeleton } from '@/components/LoadingSkeleton';
import ErrorBoundary from '@/components/ErrorBoundary';
import { ArrowUpRight, ArrowDownRight, Activity, TrendingUp, AlertTriangle, RefreshCw, ThumbsUp, ThumbsDown, Minus, Brain } from 'lucide-react';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

function SentimentCard({ sentiment }: { sentiment: { overall_sentiment: number; positive_score: number; negative_score: number; neutral_score: number; confidence: number; summary: string } }) {
  const getSentimentLabel = (score: number) => {
    if (score > 0.2) return 'Positive';
    if (score < -0.2) return 'Negative';
    return 'Neutral';
  };

  const getSentimentColor = (score: number) => {
    if (score > 0.2) return 'text-green-600';
    if (score < -0.2) return 'text-red-600';
    return 'text-gray-600';
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
        <Brain className="w-4 h-4" /> Market Sentiment
      </h3>
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className={`text-2xl font-bold ${getSentimentColor(sentiment.overall_sentiment)}`}>
            {getSentimentLabel(sentiment.overall_sentiment)}
          </div>
          <div className="text-sm text-gray-500">
            Score: {(sentiment.overall_sentiment * 100).toFixed(0)}%
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <ThumbsUp className="w-4 h-4 text-green-500" />
            <span className="text-sm text-gray-600">Positive</span>
            <div className="flex-1 bg-gray-100 rounded-full h-2">
              <div className="bg-green-500 h-2 rounded-full" style={{ width: `${sentiment.positive_score * 100}%` }}></div>
            </div>
            <span className="text-sm font-medium text-gray-700">{(sentiment.positive_score * 100).toFixed(0)}%</span>
          </div>

          <div className="flex items-center gap-2">
            <Minus className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-600">Neutral</span>
            <div className="flex-1 bg-gray-100 rounded-full h-2">
              <div className="bg-gray-400 h-2 rounded-full" style={{ width: `${sentiment.neutral_score * 100}%` }}></div>
            </div>
            <span className="text-sm font-medium text-gray-700">{(sentiment.neutral_score * 100).toFixed(0)}%</span>
          </div>

          <div className="flex items-center gap-2">
            <ThumbsDown className="w-4 h-4 text-red-500" />
            <span className="text-sm text-gray-600">Negative</span>
            <div className="flex-1 bg-gray-100 rounded-full h-2">
              <div className="bg-red-500 h-2 rounded-full" style={{ width: `${sentiment.negative_score * 100}%` }}></div>
            </div>
            <span className="text-sm font-medium text-gray-700">{(sentiment.negative_score * 100).toFixed(0)}%</span>
          </div>
        </div>

        <div className="pt-3 border-t border-gray-100">
          <p className="text-xs text-gray-500">Confidence: {(sentiment.confidence * 100).toFixed(0)}%</p>
          {sentiment.summary && (
            <p className="text-sm text-gray-600 mt-2">{sentiment.summary}</p>
          )}
        </div>
      </div>
    </div>
  );
}

function StockContent() {
  const { ticker } = useParams() as { ticker: string };
  const [retryKey, setRetryKey] = useState(0);

  const { data: report, isLoading: isReportLoading, error: reportError, refetch: refetchReport } = useQuery({
    queryKey: ['report', ticker, retryKey],
    queryFn: () => reportService.generateReport(ticker)
  });

  const { data: prediction, isLoading: isPredLoading, error: predError, refetch: refetchPrediction } = useQuery({
    queryKey: ['prediction', ticker, retryKey],
    queryFn: () => predictionService.getPrediction(ticker)
  });

  const isLoading = isReportLoading || isPredLoading;
  const hasError = reportError || predError;

  const handleRetry = () => {
    setRetryKey((k) => k + 1);
    refetchReport();
    refetchPrediction();
  };

  if (isLoading) {
    return <StockPageSkeleton />;
  }

  if (hasError) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[40vh] bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <AlertTriangle className="w-12 h-12 text-red-500 mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Failed to load data</h3>
        <p className="text-gray-600 text-sm mb-4 text-center max-w-md">
          {reportError?.message || predError?.message || 'An error occurred while fetching data for ' + ticker}
        </p>
        <button
          onClick={handleRetry}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Retry
        </button>
      </div>
    );
  }

  if (!report || !prediction) {
    return (
      <div className="text-center p-8 bg-white rounded-xl shadow-sm border border-gray-200">
        <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
        <p className="text-gray-700 font-medium">No data available for {ticker}</p>
        <button
          onClick={handleRetry}
          className="mt-4 flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors mx-auto"
        >
          <RefreshCw className="w-4 h-4" />
          Try Again
        </button>
      </div>
    );
  }

  const { company, technicalIndicators, sentiment, scoring, report_content } = report;

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{company.company_name || ticker}</h1>
            <p className="text-gray-500 font-medium">{ticker} • {company.sector || 'Equities'} • {company.exchange}</p>
          </div>
          <div className="text-right">
            <div className="text-4xl font-bold text-gray-900">${company.current_price?.toFixed(2)}</div>
            <div className="text-sm font-medium text-gray-500 mt-1">Real-time Price</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <RecommendationCard 
          score={scoring.overall_score} 
          recommendation={scoring.recommendation} 
          confidence={scoring.confidence} 
        />
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4" /> Technicals
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Trend</span>
              <span className={`font-semibold ${technicalIndicators.trend === 'Bullish' ? 'text-green-600' : technicalIndicators.trend === 'Bearish' ? 'text-red-600' : 'text-gray-600'}`}>{technicalIndicators.trend}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">RSI (14)</span>
              <span className="font-semibold">{technicalIndicators.rsi?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">MACD</span>
              <span className="font-semibold">{technicalIndicators.macd?.toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4" /> 1-Week Prediction
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-green-600 font-medium">Bullish</span>
                <span className="text-green-600 font-bold">{prediction["1_week"].bullish}%</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: `${prediction["1_week"].bullish}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-red-600 font-medium">Bearish</span>
                <span className="text-red-600 font-bold">{prediction["1_week"].bearish}%</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2">
                <div className="bg-red-500 h-2 rounded-full" style={{ width: `${prediction["1_week"].bearish}%` }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sentiment Display */}
      {sentiment && <SentimentCard sentiment={sentiment} />}

      {/* AI Investment Report with Markdown Rendering */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-blue-500" /> AI Investment Report
        </h3>
        <div className="prose prose-sm max-w-none text-gray-700">
          <ReactMarkdown>{report_content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}

export default function StockDashboard() {
  return (
    <ErrorBoundary>
      <StockContent />
    </ErrorBoundary>
  );
}
