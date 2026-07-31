import { create } from 'zustand';
import type { AIEngineResult, DataState } from '../types/contracts';

interface AIStoreState {
  aiResult: AIEngineResult | null;
  dataState: DataState;
  
  // Actions
  setAIResult: (result: AIEngineResult) => void;
  setDataState: (state: DataState) => void;
}

export const useAIStore = create<AIStoreState>((set) => ({
  aiResult: null,
  dataState: 'loading',

  setAIResult: (aiResult) =>
    set({
      aiResult,
      dataState: 'live',
    }),

  setDataState: (dataState) => set({ dataState }),
}));
