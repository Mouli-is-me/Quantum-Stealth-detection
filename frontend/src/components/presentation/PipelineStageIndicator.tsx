import React from 'react';
import { PIPELINE_STAGES, usePresentationStore } from '../../store/presentationStore';
import { clsx } from 'clsx';
import { CheckCircle2, ChevronRight } from 'lucide-react';

export const PipelineStageIndicator: React.FC = () => {
  const currentStageIndex = usePresentationStore((s) => s.currentStageIndex);
  const setCurrentStageIndex = usePresentationStore((s) => s.setCurrentStageIndex);

  return (
    <div className="w-full overflow-x-auto py-2">
      <div className="flex items-center min-w-max gap-1 font-mono text-[10px]">
        {PIPELINE_STAGES.map((stage, idx) => {
          const isActive = idx === currentStageIndex;
          const isPassed = idx < currentStageIndex;

          return (
            <React.Fragment key={stage.id}>
              <button
                onClick={() => setCurrentStageIndex(idx)}
                className={clsx(
                  'px-2.5 py-1.5 border flex items-center gap-1.5 transition-all rounded-[1px]',
                  isActive
                    ? 'bg-[#3F6B3F] border-[#5FA85F] text-[#FFFFFF] shadow-[0_0_10px_rgba(95,168,95,0.6)] font-bold'
                    : isPassed
                    ? 'bg-[#141815] border-[#35B8C4]/50 text-[#35B8C4]'
                    : 'bg-[#0A0D0A] border-[#2A322C] text-[#8A968A] hover:border-[#5FA85F]/40'
                )}
              >
                {isPassed ? (
                  <CheckCircle2 className="w-3 h-3 text-[#35B8C4]" />
                ) : (
                  <span className="w-3 h-3 border border-current text-[8px] flex items-center justify-center font-bold">
                    {idx + 1}
                  </span>
                )}
                <span>{stage.name}</span>
              </button>
              {idx < PIPELINE_STAGES.length - 1 && (
                <ChevronRight className="w-3 h-3 text-[#2A322C] shrink-0" />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
