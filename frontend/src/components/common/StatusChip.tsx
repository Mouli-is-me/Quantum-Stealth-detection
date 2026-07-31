import React from 'react';
import { clsx } from 'clsx';

interface StatusChipProps {
  status: 'online' | 'offline' | 'degraded' | 'processing' | 'error' | 'connected' | 'reconnecting' | 'disconnected' | 'none' | 'low' | 'moderate' | 'high' | 'critical';
  label?: string;
  shape?: 'square' | 'diamond' | 'circle';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const StatusChip: React.FC<StatusChipProps> = ({
  status,
  label,
  shape = 'square',
  size = 'md',
  className,
}) => {
  const getStatusColors = () => {
    switch (status) {
      case 'online':
      case 'connected':
      case 'none':
      case 'low':
        return { bg: 'bg-[#3F6B3F]', border: 'border-[#5FA85F]', glow: 'shadow-[0_0_6px_rgba(95,168,95,0.8)]', text: 'text-[#5FA85F]' };
      case 'degraded':
      case 'reconnecting':
      case 'moderate':
      case 'processing':
        return { bg: 'bg-[#D99A2B]', border: 'border-[#E5AB44]', glow: 'shadow-[0_0_6px_rgba(217,154,43,0.8)]', text: 'text-[#D99A2B]' };
      case 'critical':
      case 'high':
      case 'error':
      case 'disconnected':
        return { bg: 'bg-[#C6362F]', border: 'border-[#E74C3C]', glow: 'shadow-[0_0_6px_rgba(198,54,47,0.8)]', text: 'text-[#C6362F]' };
      case 'offline':
      default:
        return { bg: 'bg-[#4A4A4A]', border: 'border-[#666666]', glow: '', text: 'text-[#8A968A]' };
    }
  };

  const colors = getStatusColors();
  const displayLabel = label || status.toUpperCase();

  const dotSize = size === 'sm' ? 'w-2 h-2' : size === 'lg' ? 'w-3 h-3' : 'w-2.5 h-2.5';

  return (
    <div className={clsx('inline-flex items-center gap-1.5 font-mono text-xs select-none', className)}>
      <span
        className={clsx(
          dotSize,
          colors.bg,
          colors.border,
          colors.glow,
          'border transition-all duration-300',
          shape === 'diamond' ? 'rotate-45' : shape === 'circle' ? 'rounded-full' : 'rounded-[1px]'
        )}
      />
      <span className={clsx('font-semibold tracking-wider uppercase', colors.text)}>
        {displayLabel}
      </span>
    </div>
  );
};
