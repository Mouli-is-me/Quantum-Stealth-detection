import { useEffect, useRef } from 'react';
import { fetchTelemetryFrame } from '../api/endpoints';
import { useMissionStore } from '../store/missionStore';
import { useSensorStore } from '../store/sensorStore';
import { useAIStore } from '../store/aiStore';
import { useQuantumStore } from '../store/quantumStore';
import { useFusionStore } from '../store/fusionStore';
import { useLogStore } from '../store/logStore';
import { useReplayStore } from '../store/replayStore';

export function useBackendStream() {
  const setBackendConnection = useMissionStore((s) => s.setBackendConnection);
  const setMissionStatus = useMissionStore((s) => s.setMissionStatus);
  const setDataState = useMissionStore((s) => s.setDataState);
  const simulationPaused = useMissionStore((s) => s.simulationPaused);
  const isReplayActive = useReplayStore((s) => s.isReplayActive);

  const setSensors = useSensorStore((s) => s.setSensors);
  const setAIResult = useAIStore((s) => s.setAIResult);
  const setQuantumResult = useQuantumStore((s) => s.setQuantumResult);
  const setClassicalResult = useQuantumStore((s) => s.setClassicalResult);
  const setFusionResult = useFusionStore((s) => s.setFusionResult);
  const addLog = useLogStore((s) => s.addLog);
  const pushFrame = useReplayStore((s) => s.pushFrame);

  const isFirstLoad = useRef(true);

  useEffect(() => {
    let intervalId: any = null;

    async function pollTelemetry() {
      if (simulationPaused || isReplayActive) return;

      try {
        const frame = await fetchTelemetryFrame();

        setBackendConnection('connected');
        setDataState('live', null);
        setMissionStatus({
          threatLevel: frame.fusion.threatLevel,
          simulationTime: frame.timestamp,
        });

        // Dispatch data slice updates to Zustand stores
        setSensors(frame.sensors);
        setAIResult(frame.ai);
        setQuantumResult(frame.quantum);
        setClassicalResult(frame.classical);
        setFusionResult(frame.fusion);

        // Push frame to replay ring buffer
        pushFrame(frame);

        if (isFirstLoad.current) {
          addLog({
            stage: 'system',
            severity: 'info',
            message: `BACKEND CONNECTED — Telemetry pipeline active (${frame.sensors.length} dynamic sensors detected)`,
          });
          addLog({
            stage: 'quantum',
            severity: 'info',
            message: `QUBO Solver: Lowest energy = ${frame.quantum.lowestEnergy} eV, selected ${frame.quantum.selectedSensors.length} sensors`,
          });
          isFirstLoad.current = false;
        }
      } catch (err: any) {
        console.warn('[BACKEND STREAM WARN] Telemetry poll failed:', err);
        setBackendConnection('disconnected');
        setDataState('stale', err?.message || 'Backend unreachable');
      }
    }

    // Initial fetch
    pollTelemetry();

    // Poll every 3 seconds for live streaming updates
    intervalId = setInterval(pollTelemetry, 3000);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [
    simulationPaused,
    isReplayActive,
    setBackendConnection,
    setMissionStatus,
    setDataState,
    setSensors,
    setAIResult,
    setQuantumResult,
    setClassicalResult,
    setFusionResult,
    addLog,
    pushFrame,
  ]);
}
