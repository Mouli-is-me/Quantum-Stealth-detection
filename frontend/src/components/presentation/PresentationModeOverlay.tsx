import React from 'react';
import { usePresentationStore, PIPELINE_STAGES } from '../../store/presentationStore';
import { PipelineStageIndicator } from './PipelineStageIndicator';
import { X, Play, Pause, ChevronLeft, ChevronRight, Award, ShieldAlert, Zap, Cpu } from 'lucide-react';
import { useQuantumStore } from '../../store/quantumStore';
import { useAIStore } from '../../store/aiStore';
import { formatEnergy, formatNibbles } from '../../utils/formatters';

export const PresentationModeOverlay: React.FC = () => {
  const isPresentationMode = usePresentationStore((s) => s.isPresentationMode);
  const currentStageIndex = usePresentationStore((s) => s.currentStageIndex);
  const isAutoAdvancing = usePresentationStore((s) => s.isAutoAdvancing);
  const setPresentationMode = usePresentationStore((s) => s.setPresentationMode);
  const setAutoAdvancing = usePresentationStore((s) => s.setAutoAdvancing);
  const nextStage = usePresentationStore((s) => s.nextStage);
  const prevStage = usePresentationStore((s) => s.prevStage);

  const quantumResult = useQuantumStore((s) => s.quantumResult);
  const aiResult = useAIStore((s) => s.aiResult);

  if (!isPresentationMode) return null;

  const currentStage = PIPELINE_STAGES[currentStageIndex];

  return (
    <div className="fixed inset-0 z-50 bg-[#0A0D0A]/90 backdrop-blur-sm flex flex-col justify-between p-6 animate-in fade-in duration-300 font-mono">
      {/* Top Banner Controls */}
      <div className="flex justify-between items-center border-b border-[#3F6B3F] pb-3 bg-[#141815] p-3 border">
        <div className="flex items-center gap-3">
          <Award className="w-6 h-6 text-[#5FA85F] animate-pulse" />
          <div>
            <div className="text-base font-bold text-[#5FA85F] tracking-widest uppercase text-glow-green">
              JUDGE PRESENTATION MODE — LIVE PIPELINE DEMONSTRATION
            </div>
            <div className="text-[11px] text-[#8A968A]">
              Step {currentStageIndex + 1} of 9: <span className="text-[#D8E0D8] font-bold">{currentStage.name}</span> ({currentStage.code})
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setAutoAdvancing(!isAutoAdvancing)}
            className={`px-3 py-1.5 border text-xs font-bold flex items-center gap-1.5 uppercase ${
              isAutoAdvancing
                ? 'bg-[#3F6B3F]/20 border-[#5FA85F] text-[#5FA85F]'
                : 'bg-[#141815] border-[#2A322C] text-[#8A968A]'
            }`}
          >
            {isAutoAdvancing ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            {isAutoAdvancing ? 'AUTO-ADVANCE ON' : 'PAUSED'}
          </button>

          <button
            onClick={prevStage}
            className="p-1.5 bg-[#141815] border border-[#2A322C] text-[#D8E0D8] hover:border-[#5FA85F]"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          <button
            onClick={nextStage}
            className="px-3 py-1.5 bg-[#3F6B3F] border border-[#5FA85F] text-[#FFFFFF] font-bold text-xs flex items-center gap-1.5 hover:bg-[#5FA85F]"
          >
            <span>NEXT STAGE</span>
            <ChevronRight className="w-5 h-5" />
          </button>

          <button
            onClick={() => setPresentationMode(false)}
            className="p-1.5 hover:bg-[#C6362F]/20 text-[#8A968A] hover:text-[#C6362F] border border-[#2A322C]"
            title="Close Presentation Mode"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
      </div>

      {/* Middle Stage Details Callout */}
      <div className="flex-1 my-4 flex flex-col justify-center items-center">
        <div className="c2-card p-6 max-w-3xl w-full border-2 border-[#5FA85F] bg-[#141815] shadow-2xl space-y-4 c2-card-glow">
          <div className="flex justify-between items-center border-b border-[#2A322C] pb-2">
            <span className="px-2.5 py-1 bg-[#3F6B3F] text-[#FFFFFF] font-bold text-xs uppercase tracking-widest">
              ACTIVE STAGE {currentStage.id + 1} / 9
            </span>
            <span className="text-xs text-[#35B8C4] font-bold">{currentStage.code}</span>
          </div>

          <h2 className="text-2xl font-bold text-[#D8E0D8] uppercase tracking-wider text-glow-green">
            {currentStage.name}
          </h2>

          <p className="text-sm text-[#8A968A] leading-relaxed">
            {currentStage.description}
          </p>

          {/* Flash Data Callouts specific to active stage */}
          <div className="pt-2">
            {currentStage.id === 2 && aiResult && (
              <div className="bg-[#0A0D0A] p-3 border border-[#35B8C4] flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-[#35B8C4]" />
                  <span>AI PREDICTOR OUTPUT: <strong className="text-[#5FA85F]">{aiResult.prediction.label}</strong></span>
                </div>
                <span>CONFIDENCE: <strong>{(aiResult.confidence * 100).toFixed(1)}%</strong></span>
              </div>
            )}

            {(currentStage.id === 4 || currentStage.id === 5) && quantumResult && (
              <div className="bg-[#0A0D0A] p-3 border border-[#5FA85F] flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <Zap className="w-5 h-5 text-[#5FA85F]" />
                  <span>LOWEST QUBO ENERGY: <strong className="text-[#5FA85F]">{formatEnergy(quantumResult.lowestEnergy)}</strong></span>
                </div>
                <span>BITSTRING: <strong className="text-[#35B8C4]">{formatNibbles(quantumResult.bitstring)}</strong></span>
              </div>
            )}

            {currentStage.id >= 6 && (
              <div className="bg-[#0A0D0A] p-3 border border-[#D99A2B] flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <ShieldAlert className="w-5 h-5 text-[#D99A2B]" />
                  <span>TACTICAL THREAT LEVEL: <strong className="text-[#C6362F]">CRITICAL LOCK</strong></span>
                </div>
                <span>RECOMMENDED ACTION: <strong className="text-[#5FA85F]">INTERCEPT & FUSE</strong></span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Stage Progress Ribbon */}
      <div className="bg-[#141815] border border-[#2A322C] p-2">
        <PipelineStageIndicator />
      </div>
    </div>
  );
};
