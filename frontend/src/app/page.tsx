'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search } from 'lucide-react';

export default function Home() {
  const [ticker, setTicker] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker) {
      router.push(`/stock/${ticker.toUpperCase()}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
      <h1 className="text-5xl font-extrabold text-gray-900 mb-6">
        AI-Powered Stock Intelligence
      </h1>
      <p className="text-xl text-gray-600 mb-8 max-w-2xl">
        Institutional-style investment analysis powered by Machine Learning and LLMs. Enter a ticker to get started.
      </p>
      
      <form onSubmit={handleSearch} className="w-full max-w-md relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-6 w-6 text-gray-400" />
        </div>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          className="block w-full pl-12 pr-4 py-4 text-lg border-2 border-gray-200 rounded-xl bg-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors shadow-sm"
          placeholder="Enter Stock Ticker (e.g. MSFT)"
        />
        <button type="submit" className="mt-4 w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition-colors">
          Analyze Stock
        </button>
      </form>
    </div>
  );
}
