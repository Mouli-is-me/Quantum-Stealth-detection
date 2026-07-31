import React from 'react';
import { Radio } from 'lucide-react';
import { clsx } from 'clsx';

interface EmptyStateProps {
  title?: string;
  message?: string;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'NO ACTIVE SENSORS DETECTED',
  message = 'Awaiting backend sensor bus initialization or dynamic registration.',
  className,
}) => {
  return (
    <div className={clsx('c2-card p-6 flex flex-col justify-center items-center gap-2 text-center text-[#8A968A] font-mono text-xs', className)}>
      <Radio className="w-6 h-6 text-[#4A4A4A] animate-pulse" />
      <div className="font-semibold tracking-wider text-[#D8E0D8] uppercase">{title}</div>
      <div className="text-[11px] text-[#8A968A] max-w-xs">{message}</div>
    </div>
  );
};
