import clsx from 'clsx';

interface SkeletonProps {
  className?: string;
}

function Skeleton({ className }: SkeletonProps) {
  return (
    <div className={clsx('animate-pulse bg-gray-200 rounded', className)} />
  );
}

export function StockPageSkeleton() {
  return (
    <div className="space-y-6">
      {/* Header skeleton */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="flex justify-between items-start">
          <div className="space-y-3">
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-64" />
          </div>
          <div className="space-y-2 text-right">
            <Skeleton className="h-10 w-32 ml-auto" />
            <Skeleton className="h-4 w-24 ml-auto" />
          </div>
        </div>
      </div>

      {/* Cards skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <Skeleton className="h-4 w-32 mb-4" />
            <div className="space-y-4">
              <Skeleton className="h-16 w-16 rounded-full" />
              <Skeleton className="h-6 w-40" />
              <Skeleton className="h-4 w-32" />
            </div>
          </div>
        ))}
      </div>

      {/* Report skeleton */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <Skeleton className="h-6 w-48 mb-4" />
        <div className="space-y-3">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
        </div>
      </div>
    </div>
  );
}
