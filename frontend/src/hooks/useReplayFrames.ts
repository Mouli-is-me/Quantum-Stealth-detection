import { useEffect } from 'react';
import { useReplayStore } from '../store/replayStore';
import { useSensorStore } from '../store/sensorStore';
import { useAIStore } from '../store/aiStore';
import { useQuantumStore } from '../store/quantumStore';
import { useFusionStore } from '../store/fusionStore';
import { useMissionStore } from '../store/missionStore';

export function useReplayFrames() {
  const isReplayActive = useReplayStore((s) => s.isReplayActive);
  const replayFrames = useReplayStore((s) => s.replayFrames);
  const currentFrameIndex = useReplayStore((s) => s.currentFrameIndex);
  const isPlaying = useReplayStore((s) => s.isPlaying);
  const playbackSpeed = useReplayStore((s) => s.playbackSpeed);
  const setCurrentFrameIndex = useReplayStore((s) => s.setCurrentFrameIndex);

  const setSensors = useSensorStore((s) => s.setSensors);
  const setAIResult = useAIStore((s) => s.setAIResult);
  const setQuantumResult = useQuantumStore((s) => s.setQuantumResult);
  const setClassicalResult = useQuantumStore((s) => s.setClassicalResult);
  const setFusionResult = useFusionStore((s) => s.setFusionResult);
  const setMissionStatus = useMissionStore((s) => s.setMissionStatus);

  // Sync active stores with current historical frame when in replay mode
  useEffect(() => {
    if (!isReplayActive || replayFrames.length === 0) return;

    const frame = replayFrames[currentFrameIndex] || replayFrames[replayFrames.length - 1];
    if (!frame) return;

    setSensors(frame.sensors);
    setAIResult(frame.ai);
    setQuantumResult(frame.quantum);
    setClassicalResult(frame.classical);
    setFusionResult(frame.fusion);
    setMissionStatus({
      threatLevel: frame.fusion.threatLevel,
      simulationTime: frame.timestamp,
    });
  }, [
    isReplayActive,
    replayFrames,
    currentFrameIndex,
    setSensors,
    setAIResult,
    setQuantumResult,
    setClassicalResult,
    setFusionResult,
    setMissionStatus,
  ]);

  // Playback timer tick
  useEffect(() => {
    if (!isReplayActive || !isPlaying || replayFrames.length === 0) return;

    const intervalMs = Math.max(200, 1000 / playbackSpeed);
    const id = setInterval(() => {
      useReplayStore.getState().setCurrentFrameIndex(
        (useReplayStore.getState().currentFrameIndex + 1) % replayFrames.length
      );
    }, intervalMs);

    return () => clearInterval(id);
  }, [isReplayActive, isPlaying, playbackSpeed, replayFrames.length, setCurrentFrameIndex]);
}
