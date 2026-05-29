'use client';
import { useQuery } from '@tanstack/react-query';
import { stockService, predictionService, reportService } from '@/services/api';
import RecommendationCard from '@/components/cards/RecommendationCard';
import { ArrowUpRight, ArrowDownRight, Activity, TrendingUp, AlertTriangle } from 'lucide-react';
import { useParams } from 'next/navigation';

export default function StockDashboard() {
  const { ticker } = useParams() as { ticker: string };

  const { data: report, isLoading: isReportLoading } = useQuery({
    queryKey: ['report', ticker],
    queryFn: () => reportService.generateReport(ticker)
  });

  const { data: prediction, isLoading: isPredLoading } = useQuery({
    queryKey: ['prediction', ticker],
    queryFn: () => predictionService.getPrediction(ticker)
  });

  if (isReportLoading || isPredLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div>
        <p className="text-gray-600 font-medium">Analyzing {ticker}...</p>
      </div>
    );
  }

  if (!report || !prediction) {
    return <div className="text-center text-red-500 p-8">Failed to load data for {ticker}</div>;
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

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-blue-500" /> AI Investment Report
        </h3>
        <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
          {report_content}
        </div>
      </div>
    </div>
  );
}
