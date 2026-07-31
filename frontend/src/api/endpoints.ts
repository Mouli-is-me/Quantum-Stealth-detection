import { ApiClient } from './client';
import { normalizeFlaskPayload } from './schemas';
import type {
  SensorTelemetry,
  AIEngineResult,
  QuantumEngineResult,
  ClassicalBaselineResult,
  FusionResult,
  ReplayFrame
} from '../types/contracts';

/**
 * Service Endpoints Layer - Typed methods calling ApiClient
 */

export async function fetchTelemetryFrame(): Promise<ReplayFrame> {
  const rawData = await ApiClient.fetchJson<unknown>('/api/telemetry');
  return normalizeFlaskPayload(rawData);
}

export async function getSensorTelemetry(): Promise<SensorTelemetry[]> {
  const frame = await fetchTelemetryFrame();
  return frame.sensors;
}

export async function getAIEngineResult(): Promise<AIEngineResult> {
  const frame = await fetchTelemetryFrame();
  return frame.ai;
}

export async function getQuantumRunResult(): Promise<QuantumEngineResult> {
  const frame = await fetchTelemetryFrame();
  return frame.quantum;
}

export async function getClassicalBaselineResult(): Promise<ClassicalBaselineResult> {
  const frame = await fetchTelemetryFrame();
  return frame.classical;
}

export async function getFusionResult(): Promise<FusionResult> {
  const frame = await fetchTelemetryFrame();
  return frame.fusion;
}

export async function triggerSimulationScenario(): Promise<ReplayFrame> {
  // Trigger new calculation scenario via API endpoint
  const rawData = await ApiClient.fetchJson<unknown>('/api/telemetry', {
    method: 'GET', // or POST if backend endpoint extended
  });
  return normalizeFlaskPayload(rawData);
}
