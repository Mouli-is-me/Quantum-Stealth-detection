import React, { useState, useEffect } from 'react';
import { useMissionStore } from '../../store/missionStore';
import { usePresentationStore } from '../../store/presentationStore';
import { StatusChip } from '../common/StatusChip';
import { Play, Pause, RotateCcw, Award, ShieldAlert, Zap, Cpu, Radio } from 'lucide-react';
import { triggerSimulationScenario } from '../../api/endpoints';

export const TopHeader: React.FC = () => {
  const missionStatus = useMissionStore((s) => s.missionStatus);
  const simulationPaused = useMissionStore((s) => s.simulationPaused);
  const setSimulationPaused = useMissionStore((s) => s.setSimulationPaused);
  const setPresentationMode = usePresentationStore((s) => s.setPresentationMode);

  const [clock, setClock] = useState(new Date().toISOString());
  const [isTriggering, setIsTriggering] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setClock(new Date().toISOString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleTriggerScenario = async () => {
    try {
      setIsTriggering(true);
      await triggerSimulationScenario();
    } catch (err) {
      console.error('Failed to trigger backend simulation scenario:', err);
    } finally {
      setIsTriggering(false);
    }
  };

  return (
    <header className="h-14 bg-[#141815] border-b border-[#2A322C] px-4 flex items-center justify-between select-none font-mono z-40">
      {/* Title & Callsign */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-[#3F6B3F]/20 border border-[#5FA85F] flex items-center justify-center rounded-[1px]">
          <ShieldAlert className="w-5 h-5 text-[#5FA85F] animate-pulse" />
        </div>
        <div>
          <h1 className="text-sm font-bold tracking-widest text-[#D8E0D8] uppercase text-glow-green">
            QUANTUM SENSOR FUSION — STEALTH DETECTION
          </h1>
          <div className="text-[9px] text-[#8A968A] tracking-widest uppercase">
            MILITARY C2 CONSOLE // NORAD-IADS SPEC 8.4
          </div>
        </div>
      </div>

      {/* Status Lights Cluster */}
      <div className="flex items-center gap-4 bg-[#0A0D0A] px-3 py-1 border border-[#2A322C]">
        <div className="flex items-center gap-1.5" title="Threat Level">
          <StatusChip status={missionStatus.threatLevel} label={`THREAT: ${missionStatus.threatLevel}`} shape="diamond" />
        </div>
        <div className="w-[1px] h-4 bg-[#2A322C]" />
        <div className="flex items-center gap-1.5" title="AI Engine">
          <Cpu className="w-3.5 h-3.5 text-[#35B8C4]" />
          <StatusChip status={missionStatus.aiStatus} label="AI ENGINE" size="sm" />
        </div>
        <div className="w-[1px] h-4 bg-[#2A322C]" />
        <div className="flex items-center gap-1.5" title="Quantum Engine">
          <Zap className="w-3.5 h-3.5 text-[#5FA85F]" />
          <StatusChip status={missionStatus.quantumStatus} label="QUANTUM ENGINE" size="sm" />
        </div>
        <div className="w-[1px] h-4 bg-[#2A322C]" />
        <div className="flex items-center gap-1.5" title="Backend Stream">
          <Radio className="w-3.5 h-3.5 text-[#D8E0D8]" />
          <StatusChip status={missionStatus.backendConnection} label={missionStatus.backendConnection} size="sm" />
        </div>
      </div>

      {/* Controls & Clock Cluster */}
      <div className="flex items-center gap-3">
        {/* Simulation Controls */}
        <div className="flex items-center gap-1 bg-[#0A0D0A] p-1 border border-[#2A322C]">
          <button
            onClick={() => setSimulationPaused(!simulationPaused)}
            className={`px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider border flex items-center gap-1 transition-colors ${
              simulationPaused
                ? 'bg-[#D99A2B]/20 border-[#D99A2B] text-[#D99A2B]'
                : 'bg-[#3F6B3F]/20 border-[#5FA85F] text-[#5FA85F]'
            }`}
          >
            {simulationPaused ? <Play className="w-3 h-3" /> : <Pause className="w-3 h-3" />}
            {simulationPaused ? 'RESUME' : 'PAUSE'}
          </button>
          <button
            onClick={handleTriggerScenario}
            disabled={isTriggering}
            className="px-2 py-0.5 bg-[#141815] hover:bg-[#2A322C] border border-[#2A322C] text-[#D8E0D8] text-[10px] font-bold uppercase tracking-wider flex items-center gap-1 disabled:opacity-50"
            title="Generate New Scenario via Backend API"
          >
            <RotateCcw className="w-3 h-3" />
            NEW SCENARIO
          </button>
        </div>

        {/* Presentation Mode Toggle */}
        <button
          onClick={() => setPresentationMode(true)}
          className="px-3 py-1 bg-[#3F6B3F] hover:bg-[#5FA85F] border border-[#5FA85F] text-[#FFFFFF] text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 shadow-[0_0_8px_rgba(95,168,95,0.4)] transition-all"
        >
          <Award className="w-4 h-4" />
          PRESENTATION MODE
        </button>

        {/* Live Clock */}
        <div className="text-right text-[10px] font-bold text-[#D8E0D8] bg-[#0A0D0A] px-2 py-1 border border-[#2A322C]">
          <div className="text-[8px] text-[#8A968A] uppercase">ZULU TIME</div>
          {clock.split('T')[1].slice(0, 8)}
        </div>
      </div>
    </header>
  );
};
