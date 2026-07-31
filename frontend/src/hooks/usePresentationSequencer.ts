import { useEffect } from 'react';
import { usePresentationStore, PIPELINE_STAGES } from '../store/presentationStore';
import { useLogStore } from '../store/logStore';

export function usePresentationSequencer() {
  const isPresentationMode = usePresentationStore((s) => s.isPresentationMode);
  const currentStageIndex = usePresentationStore((s) => s.currentStageIndex);
  const isAutoAdvancing = usePresentationStore((s) => s.isAutoAdvancing);
  const stepIntervalMs = usePresentationStore((s) => s.stepIntervalMs);
  const nextStage = usePresentationStore((s) => s.nextStage);
  const addLog = useLogStore((s) => s.addLog);

  // Log active stage transition
  useEffect(() => {
    if (!isPresentationMode) return;

    const stage = PIPELINE_STAGES[currentStageIndex];
    if (stage) {
      addLog({
        stage: 'system',
        severity: 'info',
        message: `[PRESENTATION MODE] Pipeline Step ${stage.id + 1}/9: ${stage.name} (${stage.code})`,
      });
    }
  }, [isPresentationMode, currentStageIndex, addLog]);

  // Auto-advance stepper timer
  useEffect(() => {
    if (!isPresentationMode || !isAutoAdvancing) return;

    const timer = setInterval(() => {
      nextStage();
    }, stepIntervalMs);

    return () => clearInterval(timer);
  }, [isPresentationMode, isAutoAdvancing, stepIntervalMs, nextStage]);
}
