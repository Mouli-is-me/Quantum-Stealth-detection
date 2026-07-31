import React, { useState, useEffect, useRef } from 'react';
import { Shield, Cpu, Activity, Zap, ShieldAlert, CheckCircle, Navigation, Radio, Terminal, History, Search, ChevronDown, ChevronUp } from 'lucide-react';

interface SensorReading {
  name: string;
  value: number;
  noise: number;
}

interface DemoData {
  weather: string;
  visibility: number;
  noise: number;
  wind: number;
  temp: number;
  stealth: number;
  rawSensors: SensorReading[];
  aiConfidences: Record<string, number>;
  quantumWeights: Record<string, number>;
  fusedConfidence: number;
  threatLevel: string;
  classification: string;
  recommendedAction: string;
}

interface HistoryRecord {
  id: string;
  timestamp: string;
  targetType: 'Stealth Submarine' | 'Normal Submarine' | 'No Target';
  overallConfidence: number;
  threatLevel: string;
  radarConfidence: number;
  infraredConfidence: number;
  acousticConfidence: number;
  magneticConfidence: number;
  quantumWeights: Record<string, number>;
  finalDecision: string;
  rawSensors: SensorReading[];
  weather: string;
  visibility: number;
  noise: number;
}

export const App: React.FC = () => {
  const [seconds, setSeconds] = useState(0);
  const [stage, setStage] = useState(1);
  const [data, setData] = useState<DemoData | null>(null);
  const [loopCount, setLoopCount] = useState(1);
  const [systemLogs, setSystemLogs] = useState<string[]>([]);
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'stealth' | 'normal' | 'none'>('all');
  const [expandedRecordId, setExpandedRecordId] = useState<string | null>(null);
  const radarCanvasRef = useRef<HTMLCanvasElement | null>(null);

  // Fetch scenario data once per loop cycle
  const fetchNewScenario = async () => {
    try {
      const res = await fetch('/api/telemetry');
      const payload = await res.json();
      
      if (payload && payload.success) {
        // Enforce Radar, Infrared, Acoustic, Magnetic sensors
        const rawSensors = [
          { name: 'Radar', value: payload.sensorValues?.Radar ?? Math.round(75 + Math.random() * 15), noise: Math.round((payload.environment?.noise ?? 15) + Math.random() * 5) },
          { name: 'Infrared', value: payload.sensorValues?.Infrared ?? Math.round(60 + Math.random() * 20), noise: Math.round((payload.environment?.noise ?? 15) + 3 + Math.random() * 5) },
          { name: 'Acoustic', value: payload.sensorValues?.Acoustic ?? Math.round(45 + Math.random() * 25), noise: Math.round((payload.environment?.noise ?? 15) + 6 + Math.random() * 5) },
          { name: 'Magnetic', value: Math.round(50 + Math.random() * 30), noise: Math.round((payload.environment?.noise ?? 15) + 2 + Math.random() * 4) },
        ];

        // Generate deterministic confidence values
        const aiConfidences: Record<string, number> = {
          Radar: Math.round(rawSensors[0].value * 0.9),
          Infrared: Math.round(rawSensors[1].value * 0.85),
          Acoustic: Math.round(rawSensors[2].value * 0.88),
          Magnetic: Math.round(rawSensors[3].value * 0.82),
        };

        // Resolve optimized weights from selection
        const quantumWeights: Record<string, number> = {
          Radar: (payload.selection?.Radar === 1 || payload.qubo?.selected_sensors?.includes('Radar')) ? 95 : 18,
          Infrared: (payload.selection?.Infrared === 1 || payload.qubo?.selected_sensors?.includes('Infrared')) ? 90 : 15,
          Acoustic: (payload.selection?.Acoustic === 1 || payload.qubo?.selected_sensors?.includes('Acoustic')) ? 85 : 22,
          Magnetic: Math.random() > 0.4 ? 92 : 25,
        };

        const classification = payload.threatLevel === 'CRITICAL' || payload.threatLevel === 'HIGH' 
          ? 'SU-57 Stealth Fighter' 
          : 'UAV / Recon Drone Group';

        setData({
          weather: payload.environment?.weather || 'CLEAR',
          visibility: payload.environment?.visibility || 8.5,
          noise: payload.environment?.noise || 12,
          wind: payload.environment?.wind || 12,
          temp: payload.environment?.temp || 24,
          stealth: payload.environment?.stealth || 0.8,
          rawSensors,
          aiConfidences,
          quantumWeights,
          fusedConfidence: payload.threatConfidence || 75,
          threatLevel: payload.threatLevel || 'HIGH',
          classification,
          recommendedAction: payload.recommendedAction || 'INTERCEPT',
        });

        logEvent('SYSTEM', `Fetched new battlefield scenario (Scenario ID: SEC-${Math.floor(1000 + Math.random() * 9000)})`);
      }
    } catch (e) {
      // Offline fallback parameters matching shape
      const rawSensors = [
        { name: 'Radar', value: 82, noise: 12 },
        { name: 'Infrared', value: 65, noise: 18 },
        { name: 'Acoustic', value: 40, noise: 22 },
        { name: 'Magnetic', value: 72, noise: 14 },
      ];
      const aiConfidences = { Radar: 78, Infrared: 60, Acoustic: 35, Magnetic: 68 };
      const quantumWeights = { Radar: 92, Infrared: 88, Acoustic: 20, Magnetic: 85 };

      setData({
        weather: 'RAINY',
        visibility: 3.2,
        noise: 28,
        wind: 18,
        temp: 16,
        stealth: 0.75,
        rawSensors,
        aiConfidences,
        quantumWeights,
        fusedConfidence: 84,
        threatLevel: 'CRITICAL',
        classification: 'Unidentified Low-RCS Contact',
        recommendedAction: 'INTERCEPT',
      });
      logEvent('SYSTEM', 'Using simulated backup parameters (Backend offline)');
    }
  };

  const logEvent = (stage: string, message: string) => {
    const timestamp = new Date().toTimeString().split(' ')[0];
    setSystemLogs(prev => [...prev, `[${timestamp}] [${stage}] ${message}`].slice(-6));
  };

  // Trigger scenario fetch on mount and at start of each loop
  useEffect(() => {
    fetchNewScenario();
  }, [loopCount]);

  // Demo timer runner
  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(prev => {
        const nextSec = prev + 1;
        
        // Save history record right before loop completes
        if (nextSec === 34 && data) {
          const detId = `DET-${Math.floor(1000 + Math.random() * 9000)}`;
          
          let targetType: HistoryRecord['targetType'] = 'No Target';
          if (data.fusedConfidence > 50) {
            targetType = data.stealth > 0.5 ? 'Stealth Submarine' : 'Normal Submarine';
          }

          const newRecord: HistoryRecord = {
            id: detId,
            timestamp: new Date().toTimeString().split(' ')[0],
            targetType,
            overallConfidence: data.fusedConfidence,
            threatLevel: data.threatLevel,
            radarConfidence: data.aiConfidences.Radar,
            infraredConfidence: data.aiConfidences.Infrared,
            acousticConfidence: data.aiConfidences.Acoustic,
            magneticConfidence: data.aiConfidences.Magnetic,
            quantumWeights: data.quantumWeights,
            finalDecision: data.recommendedAction,
            rawSensors: [...data.rawSensors],
            weather: data.weather,
            visibility: data.visibility,
            noise: data.noise,
          };
          setHistory(prevHist => [newRecord, ...prevHist]);
          logEvent('HISTORY', `Auto-archived detection record: ${detId}`);
        }

        if (nextSec >= 35) {
          setLoopCount(c => c + 1);
          setStage(1);
          return 0;
        }

        if (nextSec < 5) setStage(1);
        else if (nextSec < 10) setStage(2);
        else if (nextSec < 15) setStage(3);
        else if (nextSec < 20) setStage(4);
        else if (nextSec < 25) setStage(5);
        else setStage(6);

        return nextSec;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [data]);

  // Update logs when stage changes
  useEffect(() => {
    switch (stage) {
      case 1:
        logEvent('SENSOR', 'Raw telemetry frames received from sensor bus.');
        break;
      case 2:
        logEvent('PREPROC', 'Cleaning, normalizing, and encoding sensor data.');
        break;
      case 3:
        logEvent('AI_ANALYZE', 'Evaluating individual sensor accuracy and confidence.');
        break;
      case 4:
        logEvent('QUANTUM', 'Formulating QUBO matrix and running D-Wave solver.');
        break;
      case 5:
        logEvent('FUSION', 'Fusing telemetry weight coefficients using quantum selection.');
        break;
      case 6:
        logEvent('DECISION', 'Threat classification locked. Recommendation dispatched.');
        break;
    }
  }, [stage]);

  // Center Panel Radar canvas renderer
  useEffect(() => {
    const canvas = radarCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let sweepAngle = 0;

    const drawRadar = () => {
      const size = Math.min(canvas.clientWidth, canvas.clientHeight);
      canvas.width = size;
      canvas.height = size;
      const center = size / 2;
      const radius = center - 16;

      ctx.clearRect(0, 0, size, size);

      // Radar rings
      ctx.strokeStyle = '#2A322C';
      ctx.lineWidth = 1;
      [0.2, 0.4, 0.6, 0.8, 1.0].forEach(step => {
        ctx.beginPath();
        ctx.arc(center, center, radius * step, 0, Math.PI * 2);
        ctx.stroke();
      });

      // Cardinal axis
      ctx.beginPath();
      ctx.moveTo(center - radius, center);
      ctx.lineTo(center + radius, center);
      ctx.moveTo(center, center - radius);
      ctx.lineTo(center, center + radius);
      ctx.stroke();

      // Heading ticks
      ctx.fillStyle = '#5FA85F';
      ctx.font = '9px monospace';
      ctx.fillText('N', center - 3, center - radius + 10);
      ctx.fillText('S', center - 3, center + radius - 4);
      ctx.fillText('E', center + radius - 10, center + 3);
      ctx.fillText('W', center - radius + 4, center + 3);

      // Radar Sweep
      sweepAngle = (sweepAngle + 0.02) % (Math.PI * 2);
      const sweepX = center + radius * Math.cos(sweepAngle);
      const sweepY = center + radius * Math.sin(sweepAngle);

      const sweepGrad = ctx.createConicGradient(sweepAngle, center, center);
      sweepGrad.addColorStop(0, 'rgba(53, 184, 196, 0.25)');
      sweepGrad.addColorStop(0.1, 'rgba(53, 184, 196, 0.05)');
      sweepGrad.addColorStop(0.2, 'rgba(53, 184, 196, 0)');
      ctx.fillStyle = sweepGrad;
      ctx.beginPath();
      ctx.arc(center, center, radius, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = '#35B8C4';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(center, center);
      ctx.lineTo(sweepX, sweepY);
      ctx.stroke();

      if (stage >= 5 && data) {
        const targetX = center + radius * 0.5;
        const targetY = center - radius * 0.3;

        ctx.strokeStyle = 'rgba(198, 54, 47, 0.4)';
        ctx.lineWidth = 1;
        ctx.setLineDash([2, 2]);
        ctx.beginPath();
        ctx.moveTo(center, center);
        ctx.lineTo(targetX, targetY);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = '#C6362F';
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(targetX, targetY - 6);
        ctx.lineTo(targetX + 6, targetY);
        ctx.lineTo(targetX, targetY + 6);
        ctx.lineTo(targetX - 6, targetY);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#D8E0D8';
        ctx.font = 'bold 9px monospace';
        ctx.fillText('TRK-0921-STEALTH', targetX + 10, targetY + 3);
      }

      animId = requestAnimationFrame(drawRadar);
    };

    drawRadar();
    return () => cancelAnimationFrame(animId);
  }, [stage, data]);

  // Statistics calculations
  const totalDetections = history.length;
  const stealthDetectedCount = history.filter(h => h.targetType === 'Stealth Submarine').length;
  const falseAlarmsCount = history.filter(h => h.targetType === 'No Target' && h.overallConfidence > 40).length;
  const averageConfidence = totalDetections > 0
    ? Math.round(history.reduce((acc, curr) => acc + curr.overallConfidence, 0) / totalDetections)
    : 0;

  // Filter history records
  const filteredHistory = history.filter(record => {
    const matchesSearch = record.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          record.targetType.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (filterType === 'stealth') return matchesSearch && record.targetType === 'Stealth Submarine';
    if (filterType === 'normal') return matchesSearch && record.targetType === 'Normal Submarine';
    if (filterType === 'none') return matchesSearch && record.targetType === 'No Target';
    return matchesSearch;
  });

  return (
    <div className="w-screen h-screen bg-[#0A0D0A] text-[#D8E0D8] flex flex-col overflow-hidden font-mono grid-overlay relative">
      {/* Absolute pointer-events-none overlay for scanline CRT effect */}
      <div className="absolute inset-0 pointer-events-none scanline-overlay z-40" />
      {/* Top Header Banner */}
      <header className="h-14 bg-[#141815] border-b border-[#2A322C] px-4 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-[#3F6B3F]/20 border border-[#5FA85F] flex items-center justify-center">
            <Shield className="w-5 h-5 text-[#5FA85F] animate-pulse" />
          </div>
          <div>
            <h1 className="text-xs font-bold tracking-widest text-[#D8E0D8] uppercase">
              QUANTUM OPTIMIZATION & FUSION PIPELINE DEMONSTRATION
            </h1>
            <div className="text-[9px] text-[#8A968A] tracking-widest uppercase">
              AUTOMATED MISSION SEQUENCE // LOOP CYCLE: {loopCount}
            </div>
          </div>
        </div>

        {/* Global Pipeline Progress Bar */}
        <div className="w-80 bg-[#0A0D0A] border border-[#2A322C] p-[2px] rounded-[1px] relative">
          <div className="flex justify-between text-[9px] text-[#8A968A] mb-1">
            <span>PIPELINE SEQUENCE STATUS</span>
            <span>{35 - seconds}s REMAINING</span>
          </div>
          <div className="h-1.5 bg-[#141815] w-full rounded-[1px] overflow-hidden">
            <div 
              className="h-full bg-[#5FA85F] transition-all duration-1000"
              style={{ width: `${(seconds / 35) * 100}%` }}
            />
          </div>
        </div>

        {/* ONLY interactive button: Detection History */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowHistory(true)}
            className="px-3.5 py-1.5 bg-[#3F6B3F] hover:bg-[#5FA85F] border border-[#5FA85F] text-[#FFFFFF] text-xs font-bold uppercase tracking-wider flex items-center gap-2 transition-all cursor-pointer rounded-[2px]"
          >
            <History className="w-4 h-4" />
            📜 Detection History
          </button>

          <div className="text-right text-[10px] font-bold text-[#D8E0D8] bg-[#0A0D0A] px-2 py-1 border border-[#2A322C]">
            <div className="text-[8px] text-[#8A968A] uppercase">ZULU CLOCK</div>
            {new Date().toTimeString().split(' ')[0]}
          </div>
        </div>
      </header>

      {/* Main Grid: Left Column, Center Column (Radar), Right Column */}
      <div className="flex-1 flex overflow-hidden p-3 gap-3">
        {/* Left Column: Stages 1, 2, 3 */}
        <div className="w-80 flex flex-col gap-3 h-full overflow-y-auto">
          {/* Stage 1: Raw Sensor Readings */}
          <div className={`c2-card p-3 transition-all duration-500 border ${
            stage === 1 ? 'border-[#5FA85F] shadow-[0_0_10px_rgba(95,168,95,0.15)] scale-[1.01]' : 'border-[#2A322C]'
          }`}>
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-1.5 mb-2">
              <span className="font-bold text-xs flex items-center gap-1">
                <CheckCircle className={`w-3.5 h-3.5 ${stage >= 1 ? 'text-[#5FA85F]' : 'text-[#4A4A4A]'}`} />
                STAGE 1: RAW SENSORS
              </span>
              {stage >= 1 && <span className="text-[9px] text-[#5FA85F]">ACTIVE</span>}
            </div>

            <div className="space-y-2 text-[11px]">
              {data?.rawSensors.map((s) => (
                <div key={s.name} className="flex justify-between items-center bg-[#0A0D0A] p-1.5 border border-[#2A322C]">
                  <span className="text-[#8A968A]">{s.name} Reading</span>
                  <span className="font-bold text-[#D8E0D8]">{s.value}% (Noise: {s.noise}dB)</span>
                </div>
              ))}
              <div className="bg-[#0A0D0A] p-1.5 border border-[#2A322C] mt-2">
                <div className="text-[9px] text-[#8A968A] uppercase tracking-wider mb-1">Environmental Conditions</div>
                <div className="grid grid-cols-2 gap-x-2 text-[10px]">
                  <div>Weather: <span className="text-[#D8E0D8] font-bold">{data?.weather}</span></div>
                  <div>Visibility: <span className="text-[#D8E0D8] font-bold">{data?.visibility} KM</span></div>
                </div>
              </div>
            </div>
          </div>

          {/* Stage 2: Data Preprocessing */}
          <div className={`c2-card p-3 transition-all duration-500 border ${
            stage === 2 ? 'border-[#5FA85F] shadow-[0_0_10px_rgba(95,168,95,0.15)] scale-[1.01]' : 
            stage > 2 ? 'border-[#2A322C]' : 'opacity-40 border-[#2A322C]'
          }`}>
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-1.5 mb-2">
              <span className="font-bold text-xs flex items-center gap-1">
                <CheckCircle className={`w-3.5 h-3.5 ${stage >= 2 ? 'text-[#5FA85F]' : 'text-[#4A4A4A]'}`} />
                STAGE 2: PREPROCESSING
              </span>
              {stage === 2 && <span className="text-[9px] text-[#D99A2B] animate-pulse">PROCESSING</span>}
              {stage > 2 && <span className="text-[9px] text-[#5FA85F]">COMPLETE</span>}
            </div>

            <div className="space-y-2 text-[11px]">
              <div className="flex justify-between items-center">
                <span>Data Scrubbing</span>
                <span className={stage > 2 ? 'text-[#5FA85F]' : stage === 2 ? 'text-[#D99A2B]' : 'text-[#8A968A]'}>
                  {stage > 2 ? '✓ Cleaned' : stage === 2 ? 'In Progress...' : 'Awaiting'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span>Normalization</span>
                <span className={stage > 2 ? 'text-[#5FA85F]' : stage === 2 ? 'text-[#D99A2B]' : 'text-[#8A968A]'}>
                  {stage > 2 ? '✓ Scaled' : stage === 2 ? 'In Progress...' : 'Awaiting'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span>RCS Feature Extraction</span>
                <span className={stage > 2 ? 'text-[#5FA85F]' : stage === 2 ? 'text-[#D99A2B]' : 'text-[#8A968A]'}>
                  {stage > 2 ? '✓ Extracted' : stage === 2 ? 'In Progress...' : 'Awaiting'}
                </span>
              </div>
              {stage === 2 && (
                <div className="w-full h-1 bg-[#0A0D0A] relative overflow-hidden border border-[#2A322C]">
                  <div className="h-full bg-[#D99A2B] animate-pulse-fast w-3/4" />
                </div>
              )}
            </div>
          </div>

          {/* Stage 3: AI Analysis */}
          <div className={`c2-card p-3 transition-all duration-500 border ${
            stage === 3 ? 'border-[#5FA85F] shadow-[0_0_10px_rgba(95,168,95,0.15)] scale-[1.01]' : 
            stage > 3 ? 'border-[#2A322C]' : 'opacity-40 border-[#2A322C]'
          }`}>
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-1.5 mb-2">
              <span className="font-bold text-xs flex items-center gap-1">
                <CheckCircle className={`w-3.5 h-3.5 ${stage >= 3 ? 'text-[#5FA85F]' : 'text-[#4A4A4A]'}`} />
                STAGE 3: AI ANALYSIS
              </span>
              {stage === 3 && <span className="text-[9px] text-[#D99A2B]">ANALYZING</span>}
              {stage > 3 && <span className="text-[9px] text-[#5FA85F]">COMPLETE</span>}
            </div>

            <div className="space-y-2 text-[11px]">
              {stage >= 3 && data ? (
                Object.entries(data.aiConfidences).map(([key, val]) => (
                  <div key={key} className="space-y-1">
                    <div className="flex justify-between text-[10px] text-[#8A968A]">
                      <span>{key} Confidence</span>
                      <span className="text-[#D8E0D8] font-bold">{val}%</span>
                    </div>
                    <div className="h-1 bg-[#0A0D0A] border border-[#2A322C] rounded-[1px] overflow-hidden">
                      <div className="h-full bg-[#35B8C4]" style={{ width: `${val}%` }} />
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-[#8A968A] text-center py-2">Awaiting AI Preprocessor analysis</div>
              )}
            </div>
          </div>
        </div>

        {/* Center Column: Tactical Air Defense Radar */}
        <div className="flex-1 bg-[#141815] border border-[#2A322C] flex flex-col justify-between p-3 relative">
          <div className="flex justify-between items-center border-b border-[#2A322C] pb-2">
            <span className="font-bold text-xs flex items-center gap-1.5 uppercase text-[#35B8C4]">
              <Radio className="w-4 h-4" />
              TACTICAL RADAR TARGET TRACKER
            </span>
            <span className="text-[9px] text-[#8A968A]">SCAN SCALE: 100 KM</span>
          </div>

          <div className="flex-1 flex items-center justify-center my-4">
            <canvas ref={radarCanvasRef} className="max-w-[420px] max-h-[420px] w-full h-full block" />
          </div>

          {/* Console Monitor logs */}
          <div className="bg-[#0A0D0A] border border-[#2A322C] p-2 h-24 overflow-y-auto">
            <div className="text-[8px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1 flex items-center gap-1 uppercase font-bold">
              <Terminal className="w-3 h-3 text-[#5FA85F]" />
              Console Logs
            </div>
            <div className="space-y-0.5 text-[9px] font-mono text-[#D8E0D8]/80 select-text">
              {systemLogs.map((log, index) => (
                <div key={index}>{log}</div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Stages 4, 5, 6 */}
        <div className="w-96 flex flex-col gap-3 h-full overflow-y-auto">
          {/* Stage 4: Quantum Optimization */}
          <div className={`c2-card p-3 transition-all duration-500 border ${
            stage === 4 ? 'border-[#5FA85F] shadow-[0_0_10px_rgba(95,168,95,0.15)] scale-[1.01]' : 
            stage > 4 ? 'border-[#2A322C]' : 'opacity-40 border-[#2A322C]'
          }`}>
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-1.5 mb-2">
              <span className="font-bold text-xs flex items-center gap-1">
                <CheckCircle className={`w-3.5 h-3.5 ${stage >= 4 ? 'text-[#5FA85F]' : 'text-[#4A4A4A]'}`} />
                STAGE 4: QUANTUM OPTIMIZATION
              </span>
              {stage === 4 && <span className="text-[9px] text-[#D99A2B] animate-pulse">OPTIMIZING</span>}
              {stage > 4 && <span className="text-[9px] text-[#5FA85F]">COMPLETE</span>}
            </div>

            <div className="space-y-2 text-[11px]">
              {stage === 4 && (
                <div className="space-y-1 py-1.5">
                  <div className="text-[10px] text-[#D99A2B] animate-pulse">Building QUBO Matrix...</div>
                  <div className="text-[10px] text-[#D99A2B] animate-pulse">Selecting Optimal Combinations...</div>
                </div>
              )}

              {stage >= 4 && data ? (
                <div className="space-y-2">
                  <div className="text-[10px] text-[#8A968A] uppercase mb-1">Optimized Sensor Weights</div>
                  {Object.entries(data.quantumWeights).map(([key, val]) => (
                    <div key={key} className="flex justify-between items-center bg-[#0A0D0A] p-1.5 border border-[#2A322C]">
                      <span className="text-[#8A968A]">{key} Weight</span>
                      <span className="font-bold text-[#5FA85F]">{val}%</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-[#8A968A] text-center py-2">Awaiting QUBO formulation solver run</div>
              )}
            </div>
          </div>

          {/* Stage 5: Sensor Fusion */}
          <div className={`c2-card p-3 transition-all duration-500 border ${
            stage === 5 ? 'border-[#5FA85F] shadow-[0_0_10px_rgba(95,168,95,0.15)] scale-[1.01]' : 
            stage > 5 ? 'border-[#2A322C]' : 'opacity-40 border-[#2A322C]'
          }`}>
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-1.5 mb-2">
              <span className="font-bold text-xs flex items-center gap-1">
                <CheckCircle className={`w-3.5 h-3.5 ${stage >= 5 ? 'text-[#5FA85F]' : 'text-[#4A4A4A]'}`} />
                STAGE 5: SENSOR FUSION
              </span>
              {stage === 5 && <span className="text-[9px] text-[#D99A2B]">FUSING</span>}
              {stage > 5 && <span className="text-[9px] text-[#5FA85F]">COMPLETE</span>}
            </div>

            <div className="space-y-2 text-[11px]">
              {stage >= 5 && data ? (
                <div className="space-y-2">
                  <div className="text-[#D99A2B] animate-pulse mb-1 text-[10px]">Combining Optimized Sensor Outputs...</div>
                  <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                    <div className="text-[9px] text-[#8A968A] mb-1">FUSED CALCULATION SCORE</div>
                    <div className="text-base font-bold text-[#35B8C4]">{data.fusedConfidence}%</div>
                  </div>
                </div>
              ) : (
                <div className="text-[#8A968A] text-center py-2">Awaiting sensor fusion matrix calculation</div>
              )}
            </div>
          </div>

          {/* Stage 6: Final Detection Result */}
          <div className={`c2-card p-3 flex-1 flex flex-col justify-between transition-all duration-500 border ${
            stage === 6 ? 'border-[#C6362F] bg-[#1A0A0A] shadow-[0_0_15px_rgba(198,54,47,0.2)] scale-[1.01]' : 
            'opacity-40 border-[#2A322C]'
          }`}>
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-1.5 mb-2">
              <span className="font-bold text-xs flex items-center gap-1">
                <CheckCircle className={`w-3.5 h-3.5 ${stage >= 6 ? 'text-[#C6362F]' : 'text-[#4A4A4A]'}`} />
                STAGE 6: FINAL CLASSIFICATION
              </span>
              {stage === 6 && <span className="text-[9px] text-[#C6362F] animate-pulse font-bold">LOCKED</span>}
            </div>

            <div className="space-y-3 flex-1 flex flex-col justify-center">
              {stage === 6 && data ? (
                <div className="space-y-3 text-center">
                  <div className="border border-[#C6362F] p-3 bg-[#C6362F]/10 border-l-4">
                    <h3 className="text-[#C6362F] text-sm font-bold tracking-widest text-glow-red animate-pulse">
                      {data.classification.toUpperCase()} DETECTED
                    </h3>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-left text-[11px]">
                    <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                      <span className="text-[#8A968A] block text-[9px]">Threat Confidence</span>
                      <span className="text-sm font-bold text-[#D8E0D8]">{data.fusedConfidence}%</span>
                    </div>
                    <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                      <span className="text-[#8A968A] block text-[9px]">Threat level</span>
                      <span className="text-sm font-bold text-[#C6362F] uppercase">{data.threatLevel}</span>
                    </div>
                  </div>

                  <div className="bg-[#0A0D0A] p-2.5 border border-[#5FA85F] text-left text-[11px]">
                    <span className="text-[#8A968A] block text-[9px]">C2 DECISION DISPATCH</span>
                    <strong className="text-[#5FA85F] text-xs tracking-wider">{data.recommendedAction}</strong>
                  </div>
                </div>
              ) : (
                <div className="text-[#8A968A] text-center py-6">Awaiting system target classification lock</div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Detection History Side Drawer / Modal Overlay */}
      {showHistory && (
        <div className="fixed inset-0 z-50 bg-[#000000]/80 flex justify-end font-mono">
          <div className="w-[850px] bg-[#141815] border-l border-[#2A322C] h-full flex flex-col p-4 shadow-2xl overflow-hidden animate-in slide-in-from-right duration-300">
            {/* Header */}
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-3 mb-4">
              <div className="flex items-center gap-2">
                <History className="w-5 h-5 text-[#5FA85F]" />
                <span className="text-sm font-bold tracking-wider uppercase text-[#D8E0D8]">
                  📜 SESSION DETECTION HISTORY LOGS
                </span>
              </div>
              <button
                onClick={() => setShowHistory(false)}
                className="px-2.5 py-1 bg-[#C6362F]/10 hover:bg-[#C6362F]/30 border border-[#C6362F] text-[#C6362F] text-xs font-bold uppercase rounded-[2px] cursor-pointer"
              >
                ✕ Close Panel
              </button>
            </div>

            {/* Statistics Panel */}
            <div className="grid grid-cols-4 gap-3 mb-4">
              <div className="bg-[#0A0D0A] p-2.5 border border-[#2A322C]">
                <span className="text-[9px] text-[#8A968A] block uppercase">Total Detections</span>
                <span className="text-lg font-bold text-[#D8E0D8]">{totalDetections}</span>
              </div>
              <div className="bg-[#0A0D0A] p-2.5 border border-[#2A322C]">
                <span className="text-[9px] text-[#8A968A] block uppercase">Stealth Detected</span>
                <span className="text-lg font-bold text-[#C6362F]">{stealthDetectedCount}</span>
              </div>
              <div className="bg-[#0A0D0A] p-2.5 border border-[#2A322C]">
                <span className="text-[9px] text-[#8A968A] block uppercase">False Alarms</span>
                <span className="text-lg font-bold text-[#D99A2B]">{falseAlarmsCount}</span>
              </div>
              <div className="bg-[#0A0D0A] p-2.5 border border-[#2A322C]">
                <span className="text-[9px] text-[#8A968A] block uppercase">Average Confidence</span>
                <span className="text-lg font-bold text-[#5FA85F]">{averageConfidence}%</span>
              </div>
            </div>

            {/* Search & Filters Toolbar */}
            <div className="flex flex-wrap gap-3 items-center justify-between mb-3 p-2 bg-[#0A0D0A] border border-[#2A322C]">
              {/* Search */}
              <div className="relative flex-1 max-w-xs">
                <Search className="w-3.5 h-3.5 text-[#8A968A] absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  placeholder="Search Detection ID or Target Type..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-[#141815] border border-[#2A322C] rounded-[2px] pl-8 pr-3 py-1.5 text-xs text-[#D8E0D8] focus:outline-none focus:border-[#5FA85F]"
                />
              </div>

              {/* Filters */}
              <div className="flex items-center gap-1.5 text-[10px]">
                <span className="text-[#8A968A]">FILTER:</span>
                <button
                  onClick={() => setFilterType('all')}
                  className={`px-2.5 py-1 border rounded-[2px] cursor-pointer ${
                    filterType === 'all'
                      ? 'bg-[#3F6B3F] text-[#FFFFFF] border-[#5FA85F]'
                      : 'bg-[#141815] text-[#8A968A] border-[#2A322C] hover:text-[#D8E0D8]'
                  }`}
                >
                  All Detections
                </button>
                <button
                  onClick={() => setFilterType('stealth')}
                  className={`px-2.5 py-1 border rounded-[2px] cursor-pointer ${
                    filterType === 'stealth'
                      ? 'bg-[#C6362F]/20 text-[#C6362F] border-[#C6362F]'
                      : 'bg-[#141815] text-[#8A968A] border-[#2A322C] hover:text-[#D8E0D8]'
                  }`}
                >
                  Stealth Sub
                </button>
                <button
                  onClick={() => setFilterType('normal')}
                  className={`px-2.5 py-1 border rounded-[2px] cursor-pointer ${
                    filterType === 'normal'
                      ? 'bg-[#D99A2B]/20 text-[#D99A2B] border-[#D99A2B]'
                      : 'bg-[#141815] text-[#8A968A] border-[#2A322C] hover:text-[#D8E0D8]'
                  }`}
                >
                  Normal Sub
                </button>
                <button
                  onClick={() => setFilterType('none')}
                  className={`px-2.5 py-1 border rounded-[2px] cursor-pointer ${
                    filterType === 'none'
                      ? 'bg-[#4A4A4A]/20 text-[#8A968A] border-[#4A4A4A]'
                      : 'bg-[#141815] text-[#8A968A] border-[#2A322C] hover:text-[#D8E0D8]'
                  }`}
                >
                  No Target
                </button>
              </div>
            </div>

            {/* List Table */}
            <div className="flex-1 overflow-y-auto border border-[#2A322C] bg-[#0A0D0A]">
              {filteredHistory.length === 0 ? (
                <div className="text-[#8A968A] text-center py-12 text-xs">
                  NO COMPLETED DETECTION CYCLES LOGGED YET
                </div>
              ) : (
                <div className="divide-y divide-[#2A322C]">
                  {filteredHistory.map((record) => {
                    const isExpanded = expandedRecordId === record.id;
                    return (
                      <div key={record.id} className="text-[11px] hover:bg-[#141815]/50 transition-all">
                        {/* Summary Row */}
                        <div
                          onClick={() => setExpandedRecordId(isExpanded ? null : record.id)}
                          className="flex items-center justify-between p-3 cursor-pointer select-none"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-[#8A968A] font-bold">{record.timestamp}</span>
                            <span className="text-[#35B8C4] font-bold">{record.id}</span>
                            <span className={`px-2 py-0.5 border rounded-[2px] text-[10px] font-bold uppercase ${
                              record.targetType === 'Stealth Submarine' ? 'bg-[#C6362F]/10 border-[#C6362F] text-[#C6362F]' :
                              record.targetType === 'Normal Submarine' ? 'bg-[#D99A2B]/10 border-[#D99A2B] text-[#D99A2B]' :
                              'bg-[#4A4A4A]/10 border-[#2A322C] text-[#8A968A]'
                            }`}>
                              {record.targetType}
                            </span>
                          </div>

                          <div className="flex items-center gap-4">
                            <span>Confidence: <strong className="text-[#5FA85F]">{record.overallConfidence}%</strong></span>
                            <span>Threat: <strong className="uppercase text-[#C6362F]">{record.threatLevel}</strong></span>
                            <span>Decision: <strong className="text-[#5FA85F]">{record.finalDecision}</strong></span>
                            {isExpanded ? <ChevronUp className="w-4 h-4 text-[#8A968A]" /> : <ChevronDown className="w-4 h-4 text-[#8A968A]" />}
                          </div>
                        </div>

                        {/* Expandable Section */}
                        {isExpanded && (
                          <div className="p-3 bg-[#141815] border-t border-[#2A322C] space-y-3 animate-in fade-in duration-200">
                            <div className="grid grid-cols-3 gap-3">
                              {/* Raw Sensors */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                                <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                  Raw Sensors
                                </div>
                                <div className="space-y-1 text-[10px]">
                                  {record.rawSensors.map(s => (
                                    <div key={s.name} className="flex justify-between">
                                      <span className="text-[#8A968A]">{s.name}:</span>
                                      <span className="text-[#D8E0D8]">{s.value}%</span>
                                    </div>
                                  ))}
                                </div>
                              </div>

                              {/* Preprocessed Values */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                                <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                  Preprocessed Factors
                                </div>
                                <div className="space-y-1 text-[10px]">
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Weather:</span><span className="text-[#D8E0D8]">{record.weather}</span></div>
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Visibility:</span><span className="text-[#D8E0D8]">{record.visibility} KM</span></div>
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Noise level:</span><span className="text-[#D8E0D8]">{record.noise} dB</span></div>
                                </div>
                              </div>

                              {/* AI Confidence Scores */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                                <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                  AI Confidences
                                </div>
                                <div className="space-y-1 text-[10px]">
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Radar:</span><span className="text-[#35B8C4]">{record.radarConfidence}%</span></div>
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Infrared:</span><span className="text-[#35B8C4]">{record.infraredConfidence}%</span></div>
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Acoustic:</span><span className="text-[#35B8C4]">{record.acousticConfidence}%</span></div>
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Magnetic:</span><span className="text-[#35B8C4]">{record.magneticConfidence}%</span></div>
                                </div>
                              </div>
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                              {/* Quantum Optimized Weights */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                                <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                  Quantum Optimized Weights
                                </div>
                                <div className="flex flex-wrap gap-2 text-[10px]">
                                  {Object.entries(record.quantumWeights).map(([key, val]) => (
                                    <span key={key} className="px-2 py-0.5 bg-[#3F6B3F]/15 border border-[#5FA85F]/50 text-[#5FA85F]">
                                      {key}: {val}%
                                    </span>
                                  ))}
                                </div>
                              </div>

                              {/* Sensor Fusion Result */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                                <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                  Sensor Fusion Result
                                </div>
                                <div className="space-y-1 text-[10px]">
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Fused Score:</span><strong className="text-[#5FA85F]">{record.overallConfidence}%</strong></div>
                                  <div className="flex justify-between"><span className="text-[#8A968A]">Decision Status:</span><strong className="text-[#35B8C4]">{record.finalDecision}</strong></div>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
