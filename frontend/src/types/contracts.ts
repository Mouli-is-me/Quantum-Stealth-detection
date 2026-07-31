// --- Sensor telemetry (array, length = however many sensors exist) ---
export interface SensorTelemetry {
  sensorId: string;              // unique, backend-assigned — never hardcode in UI
  sensorType: string;             // e.g. "radar", "infrared", "acoustic" — rendered generically
  status: "online" | "offline" | "degraded";
  confidence: number;             // 0–1
  reliability: number;            // 0–1
  noise: number;                  // 0–1
  signalQuality: number;          // 0–1
  health: number;                 // 0–1
  waveform: number[];             // rolling buffer of recent samples for animated waveform
  position?: { range: number; bearing: number }; // polar coords for radar plotting
  lastUpdated: string;            // ISO timestamp
}

// --- AI Engine output ---
export interface AIEngineResult {
  timestamp: string;
  featuresExtracted: Record<string, number>;
  confidence: number;
  reliability: number;
  noiseEstimate: number;
  prediction: {
    label: string;
    probability: number;
  };
}

// --- Quantum Engine output ---
export interface QuantumEngineResult {
  timestamp: string;
  quboMatrix: number[][];
  bitstring: string;
  lowestEnergy: number;
  adaptiveSensorWeights: Record<string, number>; // keyed by sensorId
  selectedSensors: string[];                     // sensorIds chosen by optimization
  executionTimeMs: number;
  backend: string;                               // e.g. simulator or QPU name, as reported
  explainability?: {
    summary: string;
    contributingFactors: { factor: string; weight: number }[];
  };
}

// --- Classical baseline output (for comparison panel) ---
export interface ClassicalBaselineResult {
  timestamp: string;
  selectedSensors: string[];
  score: number;
  executionTimeMs: number;
  method: string; // e.g. "greedy", "brute-force" — as reported by backend
  accuracy?: string;
  falseAlarm?: string;
}

export interface TargetTrack {
  trackId: string;
  range: number;
  bearing: number;
  velocity?: number;
  confidence: number;
  classification: string;
}

// --- Fusion Engine output ---
export interface FusionResult {
  timestamp: string;
  fusedConfidence: number;
  threatLevel: "none" | "low" | "moderate" | "high" | "critical";
  threatClassification: string;
  targetTracks: TargetTrack[];
  decision: string; // mission-level recommendation/output text from backend
}

// --- Mission / system status (drives header) ---
export interface MissionStatus {
  missionState: "idle" | "initializing" | "running" | "paused" | "completed" | "error";
  threatLevel: "none" | "low" | "moderate" | "high" | "critical";
  aiStatus: "online" | "offline" | "processing" | "error";
  quantumStatus: "online" | "offline" | "processing" | "error";
  backendConnection: "connected" | "reconnecting" | "disconnected";
  simulationTime: string; // ISO or elapsed
}

// --- Event log entry ---
export interface LogEvent {
  id: string;
  timestamp: string;
  stage: "sensor" | "ai" | "quantum" | "classical" | "fusion" | "system";
  severity: "info" | "warning" | "critical";
  message: string;
}

// --- Replay frame (for mission replay) ---
export interface ReplayFrame {
  timestamp: string;
  sensors: SensorTelemetry[];
  ai: AIEngineResult;
  quantum: QuantumEngineResult;
  classical: ClassicalBaselineResult;
  fusion: FusionResult;
}

// Dynamic state for each panel: loading | live | stale | error | empty
export type DataState = "loading" | "live" | "stale" | "error" | "empty";
