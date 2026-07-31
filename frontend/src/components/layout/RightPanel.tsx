import React from 'react';
import { useAIStore } from '../../store/aiStore';
import { useQuantumStore } from '../../store/quantumStore';
import { FeaturePanel } from '../ai/FeaturePanel';
import { PredictionReadout } from '../ai/PredictionReadout';
import { QuboMatrix } from '../quantum/QuboMatrix';
import { BitstringDisplay } from '../quantum/BitstringDisplay';
import { SensorWeightsList } from '../quantum/SensorWeightsList';
import { ExplainabilityPanel } from '../quantum/ExplainabilityPanel';
import { Cpu, Zap } from 'lucide-react';

export const RightPanel: React.FC = () => {
  const aiResult = useAIStore((s) => s.aiResult);
  const quantumResult = useQuantumStore((s) => s.quantumResult);

  return (
    <aside className="w-96 h-full bg-[#141815] border-l border-[#2A322C] flex flex-col font-mono select-none overflow-hidden shrink-0">
      {/* Panel Header */}
      <div className="p-3 border-b border-[#2A322C] flex justify-between items-center bg-[#0A0D0A]">
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-[#5FA85F]" />
          <span className="font-bold text-xs tracking-wider text-[#D8E0D8] uppercase">
            AI & QUANTUM ENGINES
          </span>
        </div>
        <span className="text-[10px] text-[#35B8C4] font-bold">
          QPU // NEURAL DUAL PIPELINE
        </span>
      </div>

      {/* Scrollable Container */}
      <div className="flex-1 p-3 overflow-y-auto space-y-4">
        {/* UPPER HALF — AI ENGINE */}
        <section className="space-y-3">
          <div className="text-[10px] font-bold text-[#35B8C4] uppercase tracking-widest flex items-center gap-1.5 border-b border-[#2A322C] pb-1">
            <Cpu className="w-3.5 h-3.5" />
            AI PREDICTOR ENGINE
          </div>
          <PredictionReadout aiResult={aiResult} />
          <FeaturePanel aiResult={aiResult} />
        </section>

        <div className="border-t border-[#2A322C] my-2" />

        {/* LOWER HALF — QUANTUM ENGINE */}
        <section className="space-y-3">
          <div className="text-[10px] font-bold text-[#5FA85F] uppercase tracking-widest flex items-center gap-1.5 border-b border-[#2A322C] pb-1">
            <Zap className="w-3.5 h-3.5" />
            QUANTUM OPTIMIZATION ENGINE
          </div>
          <BitstringDisplay quantumResult={quantumResult} />
          <QuboMatrix quantumResult={quantumResult} />
          <SensorWeightsList quantumResult={quantumResult} />
          <ExplainabilityPanel quantumResult={quantumResult} />
        </section>
      </div>
    </aside>
  );
};
