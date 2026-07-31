import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { clsx } from 'clsx';

interface ErrorBannerProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorBanner: React.FC<ErrorBannerProps> = ({
  title = 'ENGINE TELEMETRY ERROR',
  message = 'Telemetry data stream interrupted. Stale data shown.',
  onRetry,
  className,
}) => {
  return (
    <div className={clsx('bg-[#C6362F]/10 border border-[#C6362F] p-3 text-[#C6362F] flex items-center justify-between gap-3 font-mono text-xs', className)}>
      <div className="flex items-center gap-2.5">
        <AlertTriangle className="w-4 h-4 shrink-0 text-[#C6362F] animate-pulse" />
        <div>
          <div className="font-bold tracking-wider uppercase text-[11px] text-glow-red">{title}</div>
          <div className="text-[10px] text-[#D8E0D8]/80">{message}</div>
        </div>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-2.5 py-1 bg-[#C6362F]/20 hover:bg-[#C6362F]/40 border border-[#C6362F] text-[#D8E0D8] text-[10px] font-semibold tracking-wider uppercase flex items-center gap-1 transition-colors"
        >
          <RefreshCw className="w-3 h-3" />
          RETRY
        </button>
      )}
    </div>
  );
};
