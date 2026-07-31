import React from 'react';
import { useMissionStore } from '../../store/missionStore';
import { useQuantumStore } from '../../store/quantumStore';
import { useAIStore } from '../../store/aiStore';
import { useFusionStore } from '../../store/fusionStore';
import { ClassicalComparisonPanel } from '../classical/ClassicalComparisonPanel';
import { EventLogConsole } from '../logs/EventLogConsole';
import { ReplayScrubber } from '../replay/ReplayScrubber';
import { BitstringDisplay } from '../quantum/BitstringDisplay';
import { QuboMatrix } from '../quantum/QuboMatrix';
import { FeaturePanel } from '../ai/FeaturePanel';
import { PredictionReadout } from '../ai/PredictionReadout';
import { clsx } from 'clsx';
import { Activity, Zap, Cpu, History, Terminal, Settings, Shield } from 'lucide-react';

export const BottomTabs: React.FC = () => {
  const activeTab = useMissionStore((s) => s.activeTab);
  const setActiveTab = useMissionStore((s) => s.setActiveTab);

  const quantumResult = useQuantumStore((s) => s.quantumResult);
  const classicalResult = useQuantumStore((s) => s.classicalResult);
  const aiResult = useAIStore((s) => s.aiResult);
  const fusionResult = useFusionStore((s) => s.fusionResult);

  const tabs = [
    { id: 'overview', label: 'MISSION OVERVIEW', icon: Shield },
    { id: 'quantum', label: 'QUANTUM OPTIMIZATION', icon: Zap },
    { id: 'classical', label: 'CLASSICAL VS QUANTUM', icon: Cpu },
    { id: 'ai', label: 'AI FEATURE ENGINE', icon: Activity },
    { id: 'replay', label: 'MISSION REPLAY', icon: History },
    { id: 'logs', label: 'C2 EVENT LOGS', icon: Terminal },
    { id: 'settings', label: 'SETTINGS & PREFS', icon: Settings },
  ] as const;

  return (
    <section className="h-[280px] bg-[#141815] border-t border-[#2A322C] flex flex-col font-mono select-none overflow-hidden shrink-0">
      {/* Tab Selector Bar */}
      <div className="flex bg-[#0A0D0A] border-b border-[#2A322C] overflow-x-auto">
        {tabs.map((t) => {
          const Icon = t.icon;
          const isActive = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={clsx(
                'px-4 py-2 text-xs font-bold uppercase tracking-wider flex items-center gap-2 border-r border-[#2A322C] transition-all whitespace-nowrap',
                isActive
                  ? 'bg-[#141815] text-[#5FA85F] border-b-2 border-b-[#5FA85F] text-glow-green'
                  : 'text-[#8A968A] hover:text-[#D8E0D8] hover:bg-[#141815]/60'
              )}
            >
              <Icon className={clsx('w-3.5 h-3.5', isActive ? 'text-[#5FA85F]' : 'text-[#8A968A]')} />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Body Viewport */}
      <div className="flex-1 p-3 overflow-y-auto bg-[#141815]">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-3 gap-4 text-xs font-mono">
            <div className="c2-card p-3 space-y-2">
              <div className="font-bold text-[#35B8C4] border-b border-[#2A322C] pb-1 uppercase">
                Tactical Fusion Summary
              </div>
              <div>CLASSIFICATION: <strong className="text-[#D8E0D8]">{fusionResult?.threatClassification || 'N/A'}</strong></div>
              <div>THREAT LEVEL: <strong className="text-[#C6362F]">{fusionResult?.threatLevel.toUpperCase() || 'NONE'}</strong></div>
              <div>DECISION: <strong className="text-[#5FA85F]">{fusionResult?.decision || 'MONITOR'}</strong></div>
            </div>

            <div className="c2-card p-3 space-y-2">
              <div className="font-bold text-[#5FA85F] border-b border-[#2A322C] pb-1 uppercase">
                Quantum Solvers State
              </div>
              <div>LOWEST ENERGY: <strong className="text-[#5FA85F]">{quantumResult?.lowestEnergy || 0} eV</strong></div>
              <div>BITSTRING: <strong className="text-[#35B8C4]">{quantumResult?.bitstring || '0000'}</strong></div>
              <div>QPU LATENCY: <strong className="text-[#D8E0D8]">{quantumResult?.executionTimeMs || 0} ms</strong></div>
            </div>

            <div className="c2-card p-3 space-y-2">
              <div className="font-bold text-[#D99A2B] border-b border-[#2A322C] pb-1 uppercase">
                AI Predictor Status
              </div>
              <div>ACTION: <strong className="text-[#D99A2B]">{aiResult?.prediction.label || 'MONITOR'}</strong></div>
              <div>CONFIDENCE: <strong className="text-[#5FA85F]">{((aiResult?.confidence || 0) * 100).toFixed(1)}%</strong></div>
              <div>MODEL RELIABILITY: <strong className="text-[#D8E0D8]">{((aiResult?.reliability || 0) * 100).toFixed(1)}%</strong></div>
            </div>
          </div>
        )}

        {activeTab === 'quantum' && (
          <div className="grid grid-cols-2 gap-4">
            <BitstringDisplay quantumResult={quantumResult} />
            <QuboMatrix quantumResult={quantumResult} />
          </div>
        )}

        {activeTab === 'classical' && (
          <ClassicalComparisonPanel quantumResult={quantumResult} classicalResult={classicalResult} />
        )}

        {activeTab === 'ai' && (
          <div className="grid grid-cols-2 gap-4">
            <PredictionReadout aiResult={aiResult} />
            <FeaturePanel aiResult={aiResult} />
          </div>
        )}

        {activeTab === 'replay' && <ReplayScrubber />}

        {activeTab === 'logs' && <EventLogConsole />}

        {activeTab === 'settings' && (
          <div className="c2-card p-4 max-w-xl space-y-3 font-mono text-xs">
            <div className="font-bold text-[#D8E0D8] border-b border-[#2A322C] pb-1 uppercase">
              COMMAND CONSOLE SETTINGS & DISPLAY PREFERENCES
            </div>
            <div className="space-y-2">
              <label className="flex items-center justify-between bg-[#0A0D0A] p-2 border border-[#2A322C]">
                <span>FLASK API ENDPOINT</span>
                <span className="text-[#5FA85F] font-bold">http://127.0.0.1:5000/api/telemetry</span>
              </label>
              <label className="flex items-center justify-between bg-[#0A0D0A] p-2 border border-[#2A322C]">
                <span>HIGH-PERFORMANCE ANIMATIONS</span>
                <input type="checkbox" defaultChecked className="accent-[#5FA85F]" />
              </label>
              <label className="flex items-center justify-between bg-[#0A0D0A] p-2 border border-[#2A322C]">
                <span>RADAR RANGE SCALE UNIT</span>
                <span className="text-[#35B8C4]">KILOMETERS (KM)</span>
              </label>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
