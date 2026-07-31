import React from 'react';
import type { QuantumEngineResult } from '../../types/contracts';
import { Gauge } from '../common/Gauge';
import { Info } from 'lucide-react';

interface ExplainabilityPanelProps {
  quantumResult: QuantumEngineResult | null;
}

export const ExplainabilityPanel: React.FC<ExplainabilityPanelProps> = ({ quantumResult }) => {
  if (!quantumResult || !quantumResult.explainability) return null;

  const { summary, contributingFactors } = quantumResult.explainability;

  return (
    <div className="c2-card p-3 space-y-2 font-mono">
      <div className="flex items-center gap-1.5 border-b border-[#2A322C] pb-1 text-[11px] font-bold text-[#D8E0D8] uppercase tracking-wider">
        <Info className="w-3.5 h-3.5 text-[#35B8C4]" />
        <span>QUANTUM EXPLAINABILITY & JUSTIFICATION</span>
      </div>

      <p className="text-[10px] text-[#8A968A] leading-relaxed">
        {summary}
      </p>

      <div className="space-y-1.5 pt-1 border-t border-[#2A322C]">
        <div className="text-[9px] text-[#8A968A] uppercase tracking-wider">Key Optimization Factor Weights</div>
        {contributingFactors.map((factor) => (
          <Gauge
            key={factor.factor}
            label={factor.factor}
            value={Math.abs(factor.weight)}
            showPercentage
          />
        ))}
      </div>
    </div>
  );
};
