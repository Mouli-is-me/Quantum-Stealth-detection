import { create } from 'zustand';
import type { FusionResult, DataState } from '../types/contracts';

interface FusionStoreState {
  fusionResult: FusionResult | null;
  dataState: DataState;
  
  // Actions
  setFusionResult: (result: FusionResult) => void;
  setDataState: (state: DataState) => void;
}

export const useFusionStore = create<FusionStoreState>((set) => ({
  fusionResult: null,
  dataState: 'loading',

  setFusionResult: (fusionResult) =>
    set({
      fusionResult,
      dataState: 'live',
    }),

  setDataState: (dataState) => set({ dataState }),
}));
