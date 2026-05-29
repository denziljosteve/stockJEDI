'use client';
import Link from 'next/link';
import { Search, TrendingUp } from 'lucide-react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const [ticker, setTicker] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker) {
      router.push(`/stock/${ticker.toUpperCase()}`);
    }
  };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <span className="font-bold text-xl text-gray-900">stockJEDI</span>
            </Link>
          </div>
          <div className="flex items-center flex-1 justify-center px-2 lg:ml-6 lg:justify-end">
            <form onSubmit={handleSearch} className="max-w-lg w-full lg:max-w-xs relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Search ticker (e.g., AAPL)"
              />
            </form>
          </div>
        </div>
      </div>
    </nav>
  );
}
