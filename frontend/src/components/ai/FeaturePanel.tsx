import React from 'react';
import type { AIEngineResult } from '../../types/contracts';
import { Gauge } from '../common/Gauge';

interface FeaturePanelProps {
  aiResult: AIEngineResult | null;
}

export const FeaturePanel: React.FC<FeaturePanelProps> = ({ aiResult }) => {
  if (!aiResult) {
    return (
      <div className="c2-card p-3 text-[11px] text-[#8A968A]">
        AWAITING AI FEATURE EXTRACTION...
      </div>
    );
  }

  const features = Object.entries(aiResult.featuresExtracted);

  return (
    <div className="c2-card p-3 space-y-2.5">
      <div className="flex justify-between items-center border-b border-[#2A322C] pb-1 font-bold text-[11px] tracking-wider text-[#D8E0D8] uppercase">
        <span>AI FEATURE EXTRACTION ENGINE</span>
        <span className="text-[#35B8C4] text-[10px]">NEURAL PREDICTOR v4.2</span>
      </div>

      {/* Feature Extractions Bar List */}
      <div className="space-y-1.5 max-h-36 overflow-y-auto pr-1">
        {features.map(([key, val]) => (
          <Gauge key={key} label={key} value={typeof val === 'number' ? (val > 1 ? val / 100 : val) : 0.5} />
        ))}
      </div>

      {/* Reliability & Noise Overview */}
      <div className="grid grid-cols-2 gap-2 pt-1 border-t border-[#2A322C] text-[10px]">
        <div className="bg-[#0A0D0A] p-1.5 border border-[#2A322C]">
          <span className="text-[#8A968A] block uppercase text-[9px]">Model Reliability</span>
          <span className="text-[#5FA85F] font-bold text-[12px]">{(aiResult.reliability * 100).toFixed(1)}%</span>
        </div>
        <div className="bg-[#0A0D0A] p-1.5 border border-[#2A322C]">
          <span className="text-[#8A968A] block uppercase text-[9px]">Noise Estimate</span>
          <span className="text-[#D99A2B] font-bold text-[12px]">{(aiResult.noiseEstimate * 100).toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
};
