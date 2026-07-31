import { create } from 'zustand';
import type { ReplayFrame } from '../types/contracts';

interface ReplayStoreState {
  isReplayActive: boolean;
  replayFrames: ReplayFrame[];
  currentFrameIndex: number;
  isPlaying: boolean;
  playbackSpeed: number; // 0.5x, 1x, 2x, 4x
  
  // Actions
  pushFrame: (frame: ReplayFrame) => void;
  setReplayActive: (active: boolean) => void;
  setCurrentFrameIndex: (index: number) => void;
  setIsPlaying: (playing: boolean) => void;
  setPlaybackSpeed: (speed: number) => void;
  clearReplayBuffer: () => void;
}

export const useReplayStore = create<ReplayStoreState>((set) => ({
  isReplayActive: false,
  replayFrames: [],
  currentFrameIndex: 0,
  isPlaying: false,
  playbackSpeed: 1.0,

  pushFrame: (frame) =>
    set((state) => {
      const newFrames = [...state.replayFrames, frame].slice(-100); // capped ring buffer of 100 frames
      const newIndex = state.isReplayActive ? state.currentFrameIndex : newFrames.length - 1;
      return {
        replayFrames: newFrames,
        currentFrameIndex: newIndex,
      };
    }),

  setReplayActive: (isReplayActive) =>
    set((state) => ({
      isReplayActive,
      currentFrameIndex: isReplayActive ? Math.max(0, state.replayFrames.length - 1) : state.replayFrames.length - 1,
      isPlaying: false,
    })),

  setCurrentFrameIndex: (currentFrameIndex) => set({ currentFrameIndex }),

  setIsPlaying: (isPlaying) => set({ isPlaying }),

  setPlaybackSpeed: (playbackSpeed) => set({ playbackSpeed }),

  clearReplayBuffer: () => set({ replayFrames: [], currentFrameIndex: 0 }),
}));
