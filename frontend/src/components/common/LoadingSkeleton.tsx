import React from 'react';
import { clsx } from 'clsx';

interface LoadingSkeletonProps {
  label?: string;
  className?: string;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  label = 'AWAITING TELEMETRY STREAM...',
  className,
}) => {
  return (
    <div className={clsx('c2-card p-4 flex flex-col justify-center items-center gap-3 min-h-[140px] animate-pulse', className)}>
      <div className="w-full space-y-2">
        <div className="h-3 bg-[#2A322C] w-3/4 rounded-[1px]" />
        <div className="h-2 bg-[#1A201C] w-1/2 rounded-[1px]" />
        <div className="h-6 bg-[#2A322C]/40 w-full rounded-[1px] border border-[#2A322C]" />
      </div>
      <span className="text-[#8A968A] text-[10px] font-mono tracking-wider uppercase flex items-center gap-2">
        <span className="w-2 h-2 bg-[#D99A2B] animate-ping rounded-full inline-block" />
        {label}
      </span>
    </div>
  );
};
