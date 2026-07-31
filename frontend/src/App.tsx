import React, { useState, useEffect, useRef } from 'react';
import { Shield, Cpu, Activity, Zap, ShieldAlert, CheckCircle, Navigation, Radio, Terminal, History, Search, ChevronDown, ChevronUp, Eye, Filter } from 'lucide-react';

interface SensorReading {
  name: string;
  value: number;
  noise: number;
}

interface DemoData {
  weather: string;
  visibility: string;
  noise: string;
  seaState: string;
  stealth: number;
  rawSensors: SensorReading[];
  aiConfidences: Record<string, number>;
  quantumWeights: Record<string, number>;
  fusedConfidence: number;
  threatLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | 'UNKNOWN';
  classification: string;
  recommendedAction: string;
  explainability: string;
  targetCategory: string;
}

interface HistoryRecord {
  id: string;
  timestamp: string;
  targetCategory: string;
  targetType: string;
  overallConfidence: number;
  threatLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | 'UNKNOWN';
  radarConfidence: number;
  infraredConfidence: number;
  acousticConfidence: number;
  magneticConfidence: number;
  quantumWeights: Record<string, number>;
  finalDecision: string;
  rawSensors: SensorReading[];
  weather: string;
  visibility: string;
  noise: string;
  seaState: string;
  explainability: string;
}

// Lists of target types by category
const TARGET_CATEGORIES = {
  Naval: ['Stealth Submarine', 'Conventional Submarine', 'Destroyer', 'Frigate', 'Aircraft Carrier', 'Patrol Boat', 'Missile Boat', 'Cargo Ship', 'Fishing Vessel', 'Amphibious Assault Ship'],
  Air: ['Stealth Fighter', 'Fighter Jet', 'Bomber', 'Recon Aircraft', 'Transport Aircraft', 'UAV', 'Recon Drone', 'Attack Drone', 'Helicopter', 'UAV Swarm'],
  Ground: ['Main Battle Tank', 'Armored Vehicle', 'Missile Launcher', 'Mobile Radar', 'Military Convoy', 'Air Defense System'],
  Civilian: ['Passenger Aircraft', 'Cargo Plane', 'Cargo Ship', 'Civilian Helicopter', 'Sailboat'],
  Wildlife: ['Bird', 'Bird Flock', 'Whale', 'Dolphin', 'Floating Debris', 'Sea Waves', 'Weather Balloon', 'Rain Reflection', 'Cloud Reflection'],
  Unknown: ['Unknown Contact', 'Unknown Vessel', 'Unknown Aircraft', 'Unknown Radar Echo']
};

const WEATHER_OPTIONS = ['Clear', 'Cloudy', 'Rain', 'Fog', 'Storm', 'Snow', 'Night'];
const VISIBILITY_OPTIONS = ['300 m', '700 m', '1 km', '3 km', '6 km', '10 km'];
const NOISE_OPTIONS = ['Very Low', 'Low', 'Medium', 'High', 'Extreme'];
const SEA_STATE_OPTIONS = ['Calm', 'Moderate', 'Rough', 'High Waves'];

/**
 * Procedurally generates a unique detection scenario based on target type & environment
 */
function generateProceduralDetection(seedIndex: number, specificTimestamp?: string): HistoryRecord {
  const categoryKeys = Object.keys(TARGET_CATEGORIES) as Array<keyof typeof TARGET_CATEGORIES>;
  
  // Weighted category selection: Naval (30%), Air (30%), Ground (15%), Civilian (10%), Wildlife (10%), Unknown (5%)
  const randVal = Math.random();
  let category: keyof typeof TARGET_CATEGORIES = 'Naval';
  if (randVal < 0.3) category = 'Naval';
  else if (randVal < 0.6) category = 'Air';
  else if (randVal < 0.75) category = 'Ground';
  else if (randVal < 0.85) category = 'Civilian';
  else if (randVal < 0.95) category = 'Wildlife';
  else category = 'Unknown';

  const types = TARGET_CATEGORIES[category];
  const targetType = types[Math.floor(Math.random() * types.length)];

  // Randomized environment conditions
  const weather = WEATHER_OPTIONS[Math.floor(Math.random() * WEATHER_OPTIONS.length)];
  const visibility = VISIBILITY_OPTIONS[Math.floor(Math.random() * VISIBILITY_OPTIONS.length)];
  const noise = NOISE_OPTIONS[Math.floor(Math.random() * NOISE_OPTIONS.length)];
  const seaState = SEA_STATE_OPTIONS[Math.floor(Math.random() * SEA_STATE_OPTIONS.length)];

  // Deduce Threat Level
  let threatLevel: HistoryRecord['threatLevel'] = 'MEDIUM';
  if (category === 'Wildlife') {
    threatLevel = 'LOW';
  } else if (category === 'Unknown') {
    threatLevel = 'UNKNOWN';
  } else if (category === 'Civilian') {
    threatLevel = 'LOW';
  } else {
    // Military targets
    if (targetType.includes('Stealth') || targetType.includes('Carrier') || targetType.includes('Swarm') || targetType.includes('Defense')) {
      threatLevel = 'CRITICAL';
    } else if (targetType.includes('Fighter') || targetType.includes('Bomber') || targetType.includes('Launcher') || targetType.includes('Destroyer')) {
      threatLevel = 'HIGH';
    } else {
      threatLevel = 'MEDIUM';
    }
  }

  // Base raw sensor calculations dependent on target type properties
  let baseRadar = 50;
  let baseIR = 50;
  let baseAcoustic = 50;
  let baseMagnetic = 30;

  if (targetType.includes('Stealth')) {
    baseRadar = 15;
    baseIR = 25;
    baseAcoustic = 35;
    baseMagnetic = 40;
  } else if (category === 'Air') {
    baseRadar = 80;
    baseIR = 75;
    baseAcoustic = 40;
    baseMagnetic = 15;
  } else if (category === 'Naval') {
    baseRadar = 35;
    baseIR = 30;
    baseAcoustic = 85;
    baseMagnetic = 60;
  } else if (category === 'Ground') {
    baseRadar = 70;
    baseIR = 80;
    baseAcoustic = 55;
    baseMagnetic = 50;
  } else if (category === 'Wildlife') {
    baseRadar = 10;
    baseIR = 15;
    baseAcoustic = 20;
    baseMagnetic = 5;
  }

  // Atmospheric interference penalty offsets
  if (weather === 'Storm' || weather === 'Rain') {
    baseRadar = Math.max(5, baseRadar - 20);
    baseIR = Math.max(5, baseIR - 15);
  }
  if (weather === 'Fog') {
    baseIR = Math.max(5, baseIR - 35);
  }
  if (noise === 'Extreme' || noise === 'High') {
    baseAcoustic = Math.max(5, baseAcoustic - 25);
  }

  const rawSensors: SensorReading[] = [
    { name: 'Radar', value: Math.round(baseRadar + Math.random() * 10), noise: Math.round(10 + Math.random() * 8) },
    { name: 'Infrared', value: Math.round(baseIR + Math.random() * 10), noise: Math.round(8 + Math.random() * 8) },
    { name: 'Acoustic', value: Math.round(baseAcoustic + Math.random() * 10), noise: Math.round(12 + Math.random() * 10) },
    { name: 'Magnetic', value: Math.round(baseMagnetic + Math.random() * 10), noise: Math.round(5 + Math.random() * 5) },
  ];

  // AI Confidences follow raw readings but introduce machine learning variance
  const radarConfidence = Math.round(rawSensors[0].value * 0.9 + Math.random() * 5);
  const infraredConfidence = Math.round(rawSensors[1].value * 0.88 + Math.random() * 5);
  const acousticConfidence = Math.round(rawSensors[2].value * 0.92 + Math.random() * 5);
  const magneticConfidence = Math.round(rawSensors[3].value * 0.85 + Math.random() * 5);

  // Quantum Optimization Weight calculations - adjust weights based on targets and conditions
  let qRadar = 25;
  let qInfrared = 25;
  let qAcoustic = 25;
  let qMagnetic = 25;

  if (targetType.includes('Stealth Submarine')) {
    qAcoustic = 85;
    qMagnetic = 75;
    qRadar = 15;
    qInfrared = 10;
  } else if (targetType.includes('Stealth Fighter')) {
    qRadar = 65;
    qInfrared = 80;
    qAcoustic = 10;
    qMagnetic = 15;
  } else if (category === 'Naval') {
    qAcoustic = 75;
    qMagnetic = 55;
    qRadar = 45;
  } else if (category === 'Air') {
    qRadar = 80;
    qInfrared = 70;
    qAcoustic = 15;
  } else if (category === 'Wildlife') {
    qAcoustic = 60;
    qRadar = 15;
  }

  // Climate weight adjustments
  if (weather === 'Fog') {
    qInfrared = Math.max(5, qInfrared - 40);
  }
  if (noise === 'Extreme') {
    qAcoustic = Math.max(5, qAcoustic - 30);
  }

  // Normalize quantum weights to add up to 100%
  const qSum = qRadar + qInfrared + qAcoustic + qMagnetic;
  const quantumWeights = {
    Radar: Math.round((qRadar / qSum) * 100),
    Infrared: Math.round((qInfrared / qSum) * 100),
    Acoustic: Math.round((qAcoustic / qSum) * 100),
    Magnetic: Math.round((qMagnetic / qSum) * 100),
  };

  // Sensor Fusion calculation (fused confidence score)
  const fusedScoreNumerator =
    (radarConfidence * quantumWeights.Radar) +
    (infraredConfidence * quantumWeights.Infrared) +
    (acousticConfidence * quantumWeights.Acoustic) +
    (magneticConfidence * quantumWeights.Magnetic);
  const fusedConfidence = Math.round(fusedScoreNumerator / 100);

  // AI Decision logic
  let finalDecision = 'MONITOR';
  if (threatLevel === 'LOW') {
    finalDecision = 'IGNORE';
  } else if (threatLevel === 'UNKNOWN') {
    finalDecision = 'VERIFY';
  } else if (category === 'Civilian') {
    finalDecision = fusedConfidence > 60 ? 'ESCORT' : 'MONITOR';
  } else {
    if (fusedConfidence > 80) {
      finalDecision = threatLevel === 'CRITICAL' ? 'ENGAGE' : 'INTERCEPT';
    } else if (fusedConfidence > 55) {
      finalDecision = 'TRACK';
    } else {
      finalDecision = 'CLASSIFY';
    }
  }

  // Unique explanation synthesis
  let explainability = `Classification locked on target type [${targetType}]. `;
  if (targetType.includes('Stealth')) {
    explainability += `Active radar/IR cross section returns were low; quantum QUBO solver prioritized Acoustic (${quantumWeights.Acoustic}%) and Magnetic (${quantumWeights.Magnetic}%) channels to bypass stealth signatures. `;
  } else if (category === 'Air') {
    explainability += `High radar reflectivity and thermal anomalies identified target tracking data. `;
  } else {
    explainability += `Optimal sensor weight fusion completed. `;
  }

  if (weather === 'Fog' || weather === 'Storm') {
    explainability += `Environmental noise (${noise}) and weather constraints (${weather}) successfully mitigated via quantum adaptive weight scaling.`;
  }

  const id = `DET-${Math.floor(1000 + Math.random() * 9000)}-${seedIndex}`;

  let timestamp = specificTimestamp;
  if (!timestamp) {
    // Generate timestamps backward covering several hours of surveillance
    const dateObj = new Date();
    dateObj.setMinutes(dateObj.getMinutes() - seedIndex * 14 - Math.floor(Math.random() * 5));
    timestamp = dateObj.toTimeString().split(' ')[0];
  }

  return {
    id,
    timestamp,
    targetCategory: category,
    targetType,
    overallConfidence: fusedConfidence,
    threatLevel,
    radarConfidence,
    infraredConfidence,
    acousticConfidence,
    magneticConfidence,
    quantumWeights,
    finalDecision,
    rawSensors,
    weather,
    visibility,
    noise,
    seaState,
    explainability,
  };
}

export const App: React.FC = () => {
  const [seconds, setSeconds] = useState(0);
  const [stage, setStage] = useState(1);
  const [data, setData] = useState<DemoData | null>(null);
  const [loopCount, setLoopCount] = useState(1);
  const [systemLogs, setSystemLogs] = useState<string[]>([]);
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [expandedRecordId, setExpandedRecordId] = useState<string | null>(null);

  // Search & Filter state
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [filterThreat, setFilterThreat] = useState<string>('all');
  const [filterDecision, setFilterDecision] = useState<string>('all');
  const [minConfidence, setMinConfidence] = useState<number>(0);
  const [timeFilter, setTimeFilter] = useState<string>('all'); // all, 1h, 3h

  const radarCanvasRef = useRef<HTMLCanvasElement | null>(null);

  // Pre-populate with 15 unique, historical procedural records
  useEffect(() => {
    const historicalRecords: HistoryRecord[] = [];
    for (let i = 1; i <= 15; i++) {
      historicalRecords.push(generateProceduralDetection(i));
    }
    setHistory(historicalRecords);
  }, []);

  // Fetch or generate scenario once per loop cycle
  const fetchNewScenario = async () => {
    try {
      // Map live backend values to our clean pipeline schema
      const res = await fetch('/api/telemetry');
      const payload = await res.json();
      
      if (payload && payload.success) {
        // Build unique procedural values using payload numbers to ensure unique scenarios
        const tempRecord = generateProceduralDetection(loopCount + 100, new Date().toTimeString().split(' ')[0]);
        
        setData({
          weather: payload.environment?.weather || tempRecord.weather,
          visibility: tempRecord.visibility,
          noise: tempRecord.noise,
          seaState: tempRecord.seaState,
          stealth: payload.environment?.stealth || 0.65,
          rawSensors: tempRecord.rawSensors,
          aiConfidences: {
            Radar: tempRecord.radarConfidence,
            Infrared: tempRecord.infraredConfidence,
            Acoustic: tempRecord.acousticConfidence,
            Magnetic: tempRecord.magneticConfidence,
          },
          quantumWeights: tempRecord.quantumWeights,
          fusedConfidence: tempRecord.overallConfidence,
          threatLevel: tempRecord.threatLevel,
          classification: tempRecord.targetType,
          recommendedAction: tempRecord.finalDecision,
          explainability: tempRecord.explainability,
          targetCategory: tempRecord.targetCategory,
        });

        logEvent('SYSTEM', `Locking dynamic scenario variables: ${tempRecord.id}`);
      }
    } catch (e) {
      // Fallback generator for client static build/GitHub Pages
      const tempRecord = generateProceduralDetection(loopCount + 100, new Date().toTimeString().split(' ')[0]);
      setData({
        weather: tempRecord.weather,
        visibility: tempRecord.visibility,
        noise: tempRecord.noise,
        seaState: tempRecord.seaState,
        stealth: 0.72,
        rawSensors: tempRecord.rawSensors,
        aiConfidences: {
          Radar: tempRecord.radarConfidence,
          Infrared: tempRecord.infraredConfidence,
          Acoustic: tempRecord.acousticConfidence,
          Magnetic: tempRecord.magneticConfidence,
        },
        quantumWeights: tempRecord.quantumWeights,
        fusedConfidence: tempRecord.overallConfidence,
        threatLevel: tempRecord.threatLevel,
        classification: tempRecord.targetType,
        recommendedAction: tempRecord.finalDecision,
        explainability: tempRecord.explainability,
        targetCategory: tempRecord.targetCategory,
      });
      logEvent('SYSTEM', `Procedural generator locked: ${tempRecord.id} (Static Host Mode)`);
    }
  };

  const logEvent = (stage: string, message: string) => {
    const timestamp = new Date().toTimeString().split(' ')[0];
    setSystemLogs(prev => [...prev, `[${timestamp}] [${stage}] ${message}`].slice(-6));
  };

  // Trigger scenario fetch on start of each loop
  useEffect(() => {
    fetchNewScenario();
  }, [loopCount]);

  // Demo timer runner
  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(prev => {
        const nextSec = prev + 1;
        
        // Save history record right before loop completes (at second 34)
        if (nextSec === 34 && data) {
          const newRecord: HistoryRecord = {
            id: `DET-${Math.floor(1000 + Math.random() * 9000)}-${history.length + 1}`,
            timestamp: new Date().toTimeString().split(' ')[0],
            targetCategory: data.targetCategory,
            targetType: data.classification,
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
            seaState: data.seaState,
            explainability: data.explainability,
          };
          
          setHistory(prevHist => [newRecord, ...prevHist].slice(0, 100)); // Cap logs history at 100
          logEvent('HISTORY', `Auto-archived C2 detection run: ${newRecord.id}`);
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
  }, [data, history.length]);

  // Log active stage transition
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

        // Target color based on category
        let color = '#C6362F'; // Hostile
        if (data.targetCategory === 'Civilian') color = '#35B8C4';
        else if (data.targetCategory === 'Wildlife') color = '#5FA85F';

        ctx.fillStyle = color;
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
        ctx.fillText(data.classification, targetX + 10, targetY + 3);
      }

      animId = requestAnimationFrame(drawRadar);
    };

    drawRadar();
    return () => cancelAnimationFrame(animId);
  }, [stage, data]);

  // Statistics calculations
  const totalDetections = history.length;
  const stealthCount = history.filter(h => h.targetType.includes('Stealth')).length;
  const falseAlarmsCount = history.filter(h => h.targetCategory === 'Wildlife' || h.targetCategory === 'Unknown').length;
  const averageConfidence = totalDetections > 0
    ? Math.round(history.reduce((acc, curr) => acc + curr.overallConfidence, 0) / totalDetections)
    : 0;

  // Filter history records based on search and selected settings
  const filteredHistory = history.filter(record => {
    // Search query
    const matchSearch =
      record.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      record.targetType.toLowerCase().includes(searchQuery.toLowerCase()) ||
      record.threatLevel.toLowerCase().includes(searchQuery.toLowerCase()) ||
      record.finalDecision.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchSearch) return false;

    // Filters
    if (filterCategory !== 'all' && record.targetCategory !== filterCategory) return false;
    if (filterThreat !== 'all' && record.threatLevel !== filterThreat) return false;
    if (filterDecision !== 'all' && record.finalDecision !== filterDecision) return false;
    if (record.overallConfidence < minConfidence) return false;

    // Time ranges
    if (timeFilter === '1h') {
      // Basic mock check: record was generated less than 4 entries ago
      const index = history.findIndex(h => h.id === record.id);
      if (index > 4) return false;
    } else if (timeFilter === '3h') {
      const index = history.findIndex(h => h.id === record.id);
      if (index > 10) return false;
    }

    return true;
  });

  // Threat Color Coding resolution helper
  const getThreatColor = (category: string, level: string) => {
    if (category === 'Civilian') return { text: 'text-[#35B8C4]', border: 'border-[#35B8C4]', bg: 'bg-[#35B8C4]/10' };
    if (category === 'Wildlife') return { text: 'text-[#5FA85F]', border: 'border-[#5FA85F]', bg: 'bg-[#5FA85F]/10' };
    if (category === 'Unknown') return { text: 'text-[#A55FCE]', border: 'border-[#A55FCE]', bg: 'bg-[#A55FCE]/10' };
    if (level === 'CRITICAL') return { text: 'text-[#C6362F]', border: 'border-[#C6362F]', bg: 'bg-[#C6362F]/10' };
    if (level === 'HIGH') return { text: 'text-[#D99A2B]', border: 'border-[#D99A2B]', bg: 'bg-[#D99A2B]/10' };
    return { text: 'text-[#E5AB44]', border: 'border-[#E5AB44]', bg: 'bg-[#E5AB44]/10' };
  };

  return (
    <div className="w-screen h-screen bg-[#0A0D0A] text-[#D8E0D8] flex flex-col overflow-hidden font-mono select-none grid-overlay relative">
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
              AUTOMATED SURVEILLANCE PIPELINE // LOOP CYCLE: {loopCount}
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
                <div className="text-[9px] text-[#8A968A] uppercase tracking-wider mb-1">Surveillance Conditions</div>
                <div className="grid grid-cols-2 gap-x-2 text-[10px] gap-y-1">
                  <div>Weather: <span className="text-[#D8E0D8] font-bold">{data?.weather}</span></div>
                  <div>Visibility: <span className="text-[#D8E0D8] font-bold">{data?.visibility}</span></div>
                  <div>Noise: <span className="text-[#D8E0D8] font-bold">{data?.noise}</span></div>
                  <div>Sea State: <span className="text-[#D8E0D8] font-bold">{data?.seaState}</span></div>
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
              TACTICAL SURVEILLANCE RADAR TRACKER
            </span>
            <span className="text-[9px] text-[#8A968A]">SCAN RANGE: 100 KM</span>
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
                STAGE 6: FINAL DETECTION
              </span>
              {stage === 6 && <span className="text-[9px] text-[#C6362F] animate-pulse font-bold">LOCKED</span>}
            </div>

            <div className="space-y-3 flex-1 flex flex-col justify-center">
              {stage === 6 && data ? (
                <div className="space-y-3 text-center">
                  <div className="border border-[#C6362F] p-3 bg-[#C6362F]/10 border-l-4">
                    <h3 className="text-[#C6362F] text-sm font-bold tracking-widest text-glow-red animate-pulse">
                      {data.classification.toUpperCase()} IDENTIFIED
                    </h3>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-left text-[11px]">
                    <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                      <span className="text-[#8A968A] block text-[9px]">Fused Confidence</span>
                      <span className="text-sm font-bold text-[#D8E0D8]">{data.fusedConfidence}%</span>
                    </div>
                    <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                      <span className="text-[#8A968A] block text-[9px]">Threat Level</span>
                      <span className="text-sm font-bold text-[#C6362F] uppercase">{data.threatLevel}</span>
                    </div>
                  </div>

                  <div className="bg-[#0A0D0A] p-2.5 border border-[#5FA85F] text-left text-[11px]">
                    <span className="text-[#8A968A] block text-[9px]">C2 MISSION DECISION DISPATCH</span>
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
          <div className="w-[900px] bg-[#141815] border-l border-[#2A322C] h-full flex flex-col p-4 shadow-2xl overflow-hidden animate-in slide-in-from-right duration-300">
            {/* Header */}
            <div className="flex justify-between items-center border-b border-[#2A322C] pb-3 mb-4">
              <div className="flex items-center gap-2">
                <History className="w-5 h-5 text-[#5FA85F]" />
                <span className="text-sm font-bold tracking-wider uppercase text-[#D8E0D8]">
                  📜 Surviellance C2 Detections Log
                </span>
              </div>
              <button
                onClick={() => setShowHistory(false)}
                className="px-2.5 py-1 bg-[#C6362F]/10 hover:bg-[#C6362F]/30 border border-[#C6362F] text-[#C6362F] text-xs font-bold uppercase rounded-[2px] cursor-pointer"
              >
                ✕ Close History
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
                <span className="text-lg font-bold text-[#C6362F]">{stealthCount}</span>
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

            {/* Filters Toolbar */}
            <div className="p-3 bg-[#0A0D0A] border border-[#2A322C] mb-4 space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-[#35B8C4]">
                <Filter className="w-4 h-4" />
                <span>LOG FILTERS</span>
              </div>
              
              <div className="grid grid-cols-3 gap-3">
                {/* Search */}
                <div className="relative">
                  <span className="text-[9px] text-[#8A968A] uppercase block mb-1">Search ID / Name / Level</span>
                  <Search className="w-3.5 h-3.5 text-[#8A968A] absolute left-2.5 top-7" />
                  <input
                    type="text"
                    placeholder="Search query..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-[#141815] border border-[#2A322C] rounded-[2px] pl-8 pr-3 py-1.5 text-xs text-[#D8E0D8] focus:outline-none focus:border-[#5FA85F]"
                  />
                </div>

                {/* Target Category */}
                <div>
                  <span className="text-[9px] text-[#8A968A] uppercase block mb-1">Target Category</span>
                  <select
                    value={filterCategory}
                    onChange={(e) => setFilterCategory(e.target.value)}
                    className="w-full bg-[#141815] border border-[#2A322C] text-[#D8E0D8] text-xs px-2.5 py-1.5 rounded-[2px] focus:outline-none focus:border-[#5FA85F]"
                  >
                    <option value="all">All Categories</option>
                    <option value="Naval">Naval</option>
                    <option value="Air">Air</option>
                    <option value="Ground">Ground</option>
                    <option value="Civilian">Civilian</option>
                    <option value="Wildlife">Wildlife / False Alarm</option>
                    <option value="Unknown">Unknown</option>
                  </select>
                </div>

                {/* Threat Level */}
                <div>
                  <span className="text-[9px] text-[#8A968A] uppercase block mb-1">Threat Level</span>
                  <select
                    value={filterThreat}
                    onChange={(e) => setFilterThreat(e.target.value)}
                    className="w-full bg-[#141815] border border-[#2A322C] text-[#D8E0D8] text-xs px-2.5 py-1.5 rounded-[2px] focus:outline-none focus:border-[#5FA85F]"
                  >
                    <option value="all">All Threats</option>
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="CRITICAL">CRITICAL</option>
                    <option value="UNKNOWN">UNKNOWN</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                {/* Decision */}
                <div>
                  <span className="text-[9px] text-[#8A968A] uppercase block mb-1">Decision Status</span>
                  <select
                    value={filterDecision}
                    onChange={(e) => setFilterDecision(e.target.value)}
                    className="w-full bg-[#141815] border border-[#2A322C] text-[#D8E0D8] text-xs px-2.5 py-1.5 rounded-[2px] focus:outline-none focus:border-[#5FA85F]"
                  >
                    <option value="all">All Decisions</option>
                    <option value="IGNORE">IGNORE</option>
                    <option value="MONITOR">MONITOR</option>
                    <option value="TRACK">TRACK</option>
                    <option value="VERIFY">VERIFY</option>
                    <option value="CLASSIFY">CLASSIFY</option>
                    <option value="ESCORT">ESCORT</option>
                    <option value="INTERCEPT">INTERCEPT</option>
                    <option value="ENGAGE">ENGAGE</option>
                  </select>
                </div>

                {/* Min Confidence */}
                <div>
                  <span className="text-[9px] text-[#8A968A] uppercase block mb-1">Min Confidence: {minConfidence}%</span>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={minConfidence}
                    onChange={(e) => setMinConfidence(parseInt(e.target.value))}
                    className="w-full accent-[#5FA85F] bg-[#141815] h-7 border border-[#2A322C] px-2 rounded-[2px] cursor-pointer"
                  />
                </div>

                {/* Time Range */}
                <div>
                  <span className="text-[9px] text-[#8A968A] uppercase block mb-1">Surveillance Time Window</span>
                  <select
                    value={timeFilter}
                    onChange={(e) => setTimeFilter(e.target.value)}
                    className="w-full bg-[#141815] border border-[#2A322C] text-[#D8E0D8] text-xs px-2.5 py-1.5 rounded-[2px] focus:outline-none focus:border-[#5FA85F]"
                  >
                    <option value="all">All Surveillance Logs</option>
                    <option value="1h">Last 1 Hour</option>
                    <option value="3h">Last 3 Hours</option>
                  </select>
                </div>
              </div>
            </div>

            {/* List Table */}
            <div className="flex-1 overflow-y-auto border border-[#2A322C] bg-[#0A0D0A]">
              {filteredHistory.length === 0 ? (
                <div className="text-[#8A968A] text-center py-12 text-xs">
                  NO COMPLETED DETECTION CYCLES LOGGED MATCHING FILTERS
                </div>
              ) : (
                <div className="divide-y divide-[#2A322C]">
                  {filteredHistory.map((record) => {
                    const isExpanded = expandedRecordId === record.id;
                    const style = getThreatColor(record.targetCategory, record.threatLevel);

                    return (
                      <div key={record.id} className="text-[11px] hover:bg-[#141815]/30 transition-all">
                        {/* Summary Row */}
                        <div
                          onClick={() => setExpandedRecordId(isExpanded ? null : record.id)}
                          className="flex items-center justify-between p-3 cursor-pointer select-none"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-[#8A968A] font-mono">{record.timestamp}</span>
                            <span className="text-[#35B8C4] font-bold">{record.id}</span>
                            <span className={`px-2 py-0.5 border rounded-[2px] text-[10px] font-bold uppercase ${style.bg} ${style.border} ${style.text}`}>
                              {record.targetType}
                            </span>
                          </div>

                          <div className="flex items-center gap-4">
                            <span>Conf: <strong className="text-[#5FA85F]">{record.overallConfidence}%</strong></span>
                            <span>Threat: <strong className={`uppercase ${style.text}`}>{record.threatLevel}</strong></span>
                            <span>Decision: <strong className="text-[#5FA85F]">{record.finalDecision}</strong></span>
                            {isExpanded ? <ChevronUp className="w-4 h-4 text-[#8A968A]" /> : <ChevronDown className="w-4 h-4 text-[#8A968A]" />}
                          </div>
                        </div>

                        {/* Expandable Section */}
                        {isExpanded && (
                          <div className="p-4 bg-[#141815] border-t border-[#2A322C] space-y-3 animate-in fade-in duration-200">
                            
                            {/* Environmental + Decision Info */}
                            <div className="grid grid-cols-2 gap-3">
                              <div className="bg-[#0A0D0A] p-2.5 border border-[#2A322C] space-y-1">
                                <div className="text-[9px] text-[#8A968A] uppercase font-bold border-b border-[#2A322C] pb-1 mb-1">
                                  Environmental Conditions
                                </div>
                                <div className="grid grid-cols-2 gap-1 text-[10px]">
                                  <div>Weather: <span className="text-[#D8E0D8] font-bold">{record.weather}</span></div>
                                  <div>Visibility: <span className="text-[#D8E0D8] font-bold">{record.visibility}</span></div>
                                  <div>Ambient Noise: <span className="text-[#D8E0D8] font-bold">{record.noise}</span></div>
                                  <div>Sea State: <span className="text-[#D8E0D8] font-bold">{record.seaState}</span></div>
                                </div>
                              </div>

                              <div className="bg-[#0A0D0A] p-2.5 border border-[#2A322C] space-y-1">
                                <div className="text-[9px] text-[#8A968A] uppercase font-bold border-b border-[#2A322C] pb-1 mb-1">
                                  Explainability Summary
                                </div>
                                <p className="text-[10px] text-[#8A968A] leading-relaxed">
                                  {record.explainability}
                                </p>
                              </div>
                            </div>

                            <div className="grid grid-cols-4 gap-3">
                              {/* Raw Sensors */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                                <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                  Raw Sensors
                                </div>
                                <div className="space-y-1 text-[10px]">
                                  {record.rawSensors.map(s => (
                                    <div key={s.name} className="flex justify-between">
                                      <span className="text-[#8A968A]">{s.name}:</span>
                                      <span className="text-[#D8E0D8] font-bold">{s.value}%</span>
                                    </div>
                                  ))}
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

                              {/* Quantum Weights */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C]">
                                <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                  Quantum Weights
                                </div>
                                <div className="space-y-1 text-[10px]">
                                  {Object.entries(record.quantumWeights).map(([key, val]) => (
                                    <div key={key} className="flex justify-between">
                                      <span className="text-[#8A968A]">{key}:</span>
                                      <span className="text-[#5FA85F] font-bold">{val}%</span>
                                    </div>
                                  ))}
                                </div>
                              </div>

                              {/* Sensor Fusion Result */}
                              <div className="bg-[#0A0D0A] p-2 border border-[#2A322C] flex flex-col justify-between">
                                <div>
                                  <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1.5 uppercase font-bold">
                                    Sensor Fusion
                                  </div>
                                  <div className="flex justify-between text-[10px]"><span className="text-[#8A968A]">Fused Score:</span><strong className="text-[#5FA85F]">{record.overallConfidence}%</strong></div>
                                </div>
                                <div className="mt-2 bg-[#141815] p-1 border border-[#2A322C] text-center">
                                  <span className="text-[8px] text-[#8A968A] block uppercase">Recommended Action</span>
                                  <strong className="text-[#5FA85F] text-[10px] uppercase">{record.finalDecision}</strong>
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
