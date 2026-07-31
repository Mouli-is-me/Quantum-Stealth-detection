import { create } from 'zustand';

export interface PipelineStageInfo {
  id: number;
  name: string;
  code: string;
  description: string;
  panelHighlight: 'sensors' | 'ai' | 'quantum' | 'tactical' | 'bottom';
}

export const PIPELINE_STAGES: PipelineStageInfo[] = [
  {
    id: 0,
    name: 'Sensor Acquisition',
    code: 'STAGE_01_ACQ',
    description: 'Collecting telemetry across multi-domain sensors (Radar, Infrared, Acoustic, Thermal, EO Camera).',
    panelHighlight: 'sensors',
  },
  {
    id: 1,
    name: 'Signal Preprocessing',
    code: 'STAGE_02_DSP',
    description: 'Filtering environmental noise, atmospheric clutter, and stealth jamming distortions.',
    panelHighlight: 'sensors',
  },
  {
    id: 2,
    name: 'AI Feature Extraction',
    code: 'STAGE_03_FEAT',
    description: 'Deep neural predictor extracts RCS signatures, stealth factors, and thermal anomalies.',
    panelHighlight: 'ai',
  },
  {
    id: 3,
    name: 'Reliability Analysis',
    code: 'STAGE_04_REL',
    description: 'Evaluating individual sensor signal quality, health, and dynamic confidence scores.',
    panelHighlight: 'ai',
  },
  {
    id: 4,
    name: 'QUBO Generation',
    code: 'STAGE_05_QUBO',
    description: 'Formulating Quadratic Unconstrained Binary Optimization matrix for sensor cross-correlation.',
    panelHighlight: 'quantum',
  },
  {
    id: 5,
    name: 'Quantum Optimization',
    code: 'STAGE_06_QPU',
    description: 'Executing quantum annealer solver on D-Wave QPU / quantum simulator to find minimum energy bitstring.',
    panelHighlight: 'quantum',
  },
  {
    id: 6,
    name: 'Adaptive Sensor Fusion',
    code: 'STAGE_07_FUSE',
    description: 'Weighting telemetry signals according to quantum-optimized bitstring selection.',
    panelHighlight: 'tactical',
  },
  {
    id: 7,
    name: 'Threat Classification',
    code: 'STAGE_08_CLASS',
    description: 'Determining stealth target position, velocity vector, RCS confidence, and threat tier.',
    panelHighlight: 'tactical',
  },
  {
    id: 8,
    name: 'Mission Decision',
    code: 'STAGE_09_EXEC',
    description: 'Synthesizing tactical recommendation: Intercept, Track, Monitor, or Illumination Lock.',
    panelHighlight: 'bottom',
  },
];

interface PresentationStoreState {
  isPresentationMode: boolean;
  currentStageIndex: number;
  isAutoAdvancing: boolean;
  stepIntervalMs: number;

  // Actions
  setPresentationMode: (active: boolean) => void;
  setCurrentStageIndex: (index: number) => void;
  nextStage: () => void;
  prevStage: () => void;
  setAutoAdvancing: (auto: boolean) => void;
}

export const usePresentationStore = create<PresentationStoreState>((set) => ({
  isPresentationMode: false,
  currentStageIndex: 0,
  isAutoAdvancing: true,
  stepIntervalMs: 3000,

  setPresentationMode: (isPresentationMode) =>
    set({
      isPresentationMode,
      currentStageIndex: 0,
    }),

  setCurrentStageIndex: (currentStageIndex) =>
    set({ currentStageIndex: Math.max(0, Math.min(PIPELINE_STAGES.length - 1, currentStageIndex)) }),

  nextStage: () =>
    set((state) => ({
      currentStageIndex: (state.currentStageIndex + 1) % PIPELINE_STAGES.length,
    })),

  prevStage: () =>
    set((state) => ({
      currentStageIndex: (state.currentStageIndex - 1 + PIPELINE_STAGES.length) % PIPELINE_STAGES.length,
    })),

  setAutoAdvancing: (isAutoAdvancing) => set({ isAutoAdvancing }),
}));
