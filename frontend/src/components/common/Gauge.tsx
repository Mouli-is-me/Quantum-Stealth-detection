import React from 'react';
import { clsx } from 'clsx';
import { formatPercent } from '../../utils/formatters';

interface GaugeProps {
  label: string;
  value: number; // 0 to 1
  warningThreshold?: number;
  criticalThreshold?: number;
  showPercentage?: boolean;
  unit?: string;
  className?: string;
}

export const Gauge: React.FC<GaugeProps> = ({
  label,
  value,
  warningThreshold = 0.4,
  criticalThreshold = 0.2,
  showPercentage = true,
  unit,
  className,
}) => {
  const normalizedValue = Math.max(0, Math.min(1, value));

  const getBarColor = () => {
    if (normalizedValue <= criticalThreshold) return 'bg-[#C6362F] shadow-[0_0_6px_rgba(198,54,47,0.5)]';
    if (normalizedValue <= warningThreshold) return 'bg-[#D99A2B] shadow-[0_0_6px_rgba(217,154,43,0.5)]';
    return 'bg-[#5FA85F] shadow-[0_0_6px_rgba(95,168,95,0.5)]';
  };

  return (
    <div className={clsx('space-y-1 font-mono text-[11px]', className)}>
      <div className="flex justify-between items-center text-[#8A968A]">
        <span className="uppercase tracking-wider text-[10px]">{label}</span>
        <span className="font-semibold text-[#D8E0D8]">
          {unit ? `${(normalizedValue * 100).toFixed(1)} ${unit}` : showPercentage ? formatPercent(normalizedValue) : normalizedValue.toFixed(2)}
        </span>
      </div>
      <div className="w-full h-1.5 bg-[#0A0D0A] border border-[#2A322C] p-[1px] rounded-[1px] relative overflow-hidden">
        <div
          className={clsx('h-full transition-all duration-300 rounded-[1px]', getBarColor())}
          style={{ width: `${normalizedValue * 100}%` }}
        />
      </div>
    </div>
  );
};
