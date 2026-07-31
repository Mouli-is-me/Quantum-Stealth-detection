import { create } from 'zustand';
import type { SensorTelemetry, DataState } from '../types/contracts';

interface SensorStoreState {
  sensors: SensorTelemetry[];
  dataState: DataState;
  lastUpdated: string | null;
  
  // Actions
  setSensors: (sensors: SensorTelemetry[]) => void;
  setDataState: (state: DataState) => void;
}

export const useSensorStore = create<SensorStoreState>((set) => ({
  sensors: [],
  dataState: 'loading',
  lastUpdated: null,

  setSensors: (sensors) =>
    set({
      sensors,
      dataState: 'live',
      lastUpdated: new Date().toISOString(),
    }),

  setDataState: (dataState) => set({ dataState }),
}));
