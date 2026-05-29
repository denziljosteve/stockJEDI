import clsx from 'clsx';
import { ShieldAlert, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface RecommendationCardProps {
  score: number;
  recommendation: string;
  confidence: string;
}

export default function RecommendationCard({ score, recommendation, confidence }: RecommendationCardProps) {
  const isBullish = score > 60;
  const isBearish = score < 40;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col h-full">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Investment Rating</h3>
      
      <div className="flex items-center gap-4 mb-6">
        <div className={clsx(
          "w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold",
          isBullish ? "bg-green-100 text-green-700" : isBearish ? "bg-red-100 text-red-700" : "bg-gray-100 text-gray-700"
        )}>
          {score}
        </div>
        <div>
          <div className="text-2xl font-bold text-gray-900">{recommendation}</div>
          <div className="text-sm text-gray-500 flex items-center gap-1">
            <ShieldAlert className="w-4 h-4" />
            {confidence} Confidence
          </div>
        </div>
      </div>

      <div className="mt-auto pt-4 border-t border-gray-100">
        <div className="flex items-center gap-2">
          {isBullish ? <TrendingUp className="text-green-500" /> : isBearish ? <TrendingDown className="text-red-500" /> : <Minus className="text-gray-500" />}
          <span className="text-sm font-medium text-gray-700">
            {isBullish ? "Positive Outlook" : isBearish ? "Negative Outlook" : "Neutral Outlook"}
          </span>
        </div>
      </div>
    </div>
  );
}
