import { create } from 'zustand';
import type { LogEvent } from '../types/contracts';

interface LogStoreState {
  logs: LogEvent[];
  filterStage: LogEvent['stage'] | 'all';
  filterSeverity: LogEvent['severity'] | 'all';
  
  // Actions
  addLog: (log: Omit<LogEvent, 'id' | 'timestamp'> & { timestamp?: string }) => void;
  addLogs: (newLogs: Omit<LogEvent, 'id'>[]) => void;
  clearLogs: () => void;
  setFilterStage: (stage: LogStoreState['filterStage']) => void;
  setFilterSeverity: (severity: LogStoreState['filterSeverity']) => void;
}

export const useLogStore = create<LogStoreState>((set) => ({
  logs: [
    {
      id: 'log-001',
      timestamp: new Date().toISOString(),
      stage: 'system',
      severity: 'info',
      message: 'TACTICAL COMMAND & CONTROL CONSOLE INITIALIZED',
    },
    {
      id: 'log-002',
      timestamp: new Date().toISOString(),
      stage: 'sensor',
      severity: 'info',
      message: 'MULTI-SENSOR TELEMETRY BUS CONNECTED (5 SENSORS ONLINE)',
    },
  ],
  filterStage: 'all',
  filterSeverity: 'all',

  addLog: (log) =>
    set((state) => ({
      logs: [
        ...state.logs,
        {
          timestamp: new Date().toISOString(),
          ...log,
          id: `log-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        },
      ].slice(-300), // capped at 300 entries for console performance
    })),

  addLogs: (newLogs) =>
    set((state) => ({
      logs: [
        ...state.logs,
        ...newLogs.map((log) => ({
          ...log,
          id: `log-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        })),
      ].slice(-300),
    })),

  clearLogs: () => set({ logs: [] }),

  setFilterStage: (filterStage) => set({ filterStage }),

  setFilterSeverity: (filterSeverity) => set({ filterSeverity }),
}));
