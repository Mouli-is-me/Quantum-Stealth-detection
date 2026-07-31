import { create } from 'zustand';
import type { MissionStatus, DataState } from '../types/contracts';

interface MissionStoreState {
  missionStatus: MissionStatus;
  dataState: DataState;
  errorMessage: string | null;
  activeTab: 'overview' | 'quantum' | 'classical' | 'ai' | 'replay' | 'logs' | 'settings';
  selectedSensorId: string | null;
  selectedTrackId: string | null;
  simulationPaused: boolean;
  simulationSpeed: number;
  
  // Actions
  setBackendConnection: (connection: MissionStatus['backendConnection']) => void;
  setMissionStatus: (status: Partial<MissionStatus>) => void;
  setDataState: (state: DataState, error?: string | null) => void;
  setActiveTab: (tab: MissionStoreState['activeTab']) => void;
  setSelectedSensorId: (id: string | null) => void;
  setSelectedTrackId: (id: string | null) => void;
  setSimulationPaused: (paused: boolean) => void;
  setSimulationSpeed: (speed: number) => void;
}

export const useMissionStore = create<MissionStoreState>((set) => ({
  missionStatus: {
    missionState: 'running',
    threatLevel: 'moderate',
    aiStatus: 'online',
    quantumStatus: 'online',
    backendConnection: 'disconnected',
    simulationTime: new Date().toISOString(),
  },
  dataState: 'loading',
  errorMessage: null,
  activeTab: 'overview',
  selectedSensorId: null,
  selectedTrackId: null,
  simulationPaused: false,
  simulationSpeed: 1.0,

  setBackendConnection: (connection) =>
    set((state) => ({
      missionStatus: { ...state.missionStatus, backendConnection: connection },
    })),

  setMissionStatus: (status) =>
    set((state) => ({
      missionStatus: { ...state.missionStatus, ...status },
    })),

  setDataState: (dataState, errorMessage = null) =>
    set({ dataState, errorMessage }),

  setActiveTab: (activeTab) => set({ activeTab }),

  setSelectedSensorId: (selectedSensorId) => set({ selectedSensorId }),

  setSelectedTrackId: (selectedTrackId) => set({ selectedTrackId }),

  setSimulationPaused: (simulationPaused) => set({ simulationPaused }),

  setSimulationSpeed: (simulationSpeed) => set({ simulationSpeed }),
}));
