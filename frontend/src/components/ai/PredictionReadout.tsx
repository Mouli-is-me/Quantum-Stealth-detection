import React from 'react';
import type { AIEngineResult } from '../../types/contracts';
import { clsx } from 'clsx';
import { ShieldAlert, Crosshair, Eye } from 'lucide-react';

interface PredictionReadoutProps {
  aiResult: AIEngineResult | null;
}

export const PredictionReadout: React.FC<PredictionReadoutProps> = ({ aiResult }) => {
  if (!aiResult) return null;

  const label = aiResult.prediction.label.toUpperCase();
  const prob = aiResult.prediction.probability;

  const getActionStyle = () => {
    if (label.includes('INTERCEPT') || prob > 0.8) {
      return { bg: 'bg-[#C6362F]/20', border: 'border-[#C6362F]', text: 'text-[#C6362F]', icon: ShieldAlert, glow: 'text-glow-red' };
    }
    if (label.includes('TRACK') || prob > 0.6) {
      return { bg: 'bg-[#D99A2B]/20', border: 'border-[#D99A2B]', text: 'text-[#D99A2B]', icon: Crosshair, glow: 'text-glow-amber' };
    }
    return { bg: 'bg-[#3F6B3F]/20', border: 'border-[#5FA85F]', text: 'text-[#5FA85F]', icon: Eye, glow: 'text-glow-green' };
  };

  const style = getActionStyle();
  const IconComp = style.icon;

  return (
    <div className={clsx('c2-card p-3 border border-l-4 space-y-2', style.border)}>
      <div className="flex justify-between items-center text-[10px] text-[#8A968A] uppercase tracking-wider">
        <span>AI Tactical Action Recommendation</span>
        <span className="font-mono text-[#D8E0D8]">PROBABILITY: {(prob * 100).toFixed(1)}%</span>
      </div>

      <div className={clsx('p-2.5 flex items-center justify-between', style.bg, style.border)}>
        <div className="flex items-center gap-2.5">
          <IconComp className={clsx('w-6 h-6 animate-pulse', style.text)} />
          <div>
            <div className={clsx('text-lg font-bold tracking-widest uppercase font-mono', style.text, style.glow)}>
              {label}
            </div>
            <div className="text-[10px] text-[#D8E0D8]/80 font-mono">
              TARGET CLASSIFICATION LOCKED
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-[10px] text-[#8A968A] uppercase font-mono">CONFIDENCE</div>
          <div className="text-base font-bold font-mono text-[#D8E0D8]">
            {(aiResult.confidence * 100).toFixed(1)}%
          </div>
        </div>
      </div>
    </div>
  );
};
