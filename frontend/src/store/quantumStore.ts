import { create } from 'zustand';
import type { QuantumEngineResult, ClassicalBaselineResult, DataState } from '../types/contracts';

interface QuantumStoreState {
  quantumResult: QuantumEngineResult | null;
  classicalResult: ClassicalBaselineResult | null;
  dataState: DataState;
  
  // Actions
  setQuantumResult: (result: QuantumEngineResult) => void;
  setClassicalResult: (result: ClassicalBaselineResult) => void;
  setDataState: (state: DataState) => void;
}

export const useQuantumStore = create<QuantumStoreState>((set) => ({
  quantumResult: null,
  classicalResult: null,
  dataState: 'loading',

  setQuantumResult: (quantumResult) =>
    set({
      quantumResult,
      dataState: 'live',
    }),

  setClassicalResult: (classicalResult) =>
    set({ classicalResult }),

  setDataState: (dataState) => set({ dataState }),
}));
