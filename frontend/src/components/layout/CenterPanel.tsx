import React, { useState } from 'react';
import { useFusionStore } from '../../store/fusionStore';
import { useSensorStore } from '../../store/sensorStore';
import { RadarCanvas } from '../tactical/RadarCanvas';
import { Crosshair, Layers, ShieldAlert, Navigation } from 'lucide-react';
import { StatusChip } from '../common/StatusChip';

export const CenterPanel: React.FC = () => {
  const fusionResult = useFusionStore((s) => s.fusionResult);
  const sensors = useSensorStore((s) => s.sensors);
  const [showHeatmap, setShowHeatmap] = useState(true);

  return (
    <main className="flex-1 h-full bg-[#0A0D0A] flex flex-col justify-between p-3 overflow-hidden select-none font-mono relative">
      {/* Tactical Display Toolbar Header */}
      <div className="flex justify-between items-center bg-[#141815] border border-[#2A322C] px-3 py-2 z-10">
        <div className="flex items-center gap-2">
          <Crosshair className="w-4 h-4 text-[#35B8C4]" />
          <span className="font-bold text-xs tracking-wider text-[#D8E0D8] uppercase">
            TACTICAL DISPLAY — SECTOR AIR DEFENSE RADAR
          </span>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowHeatmap(!showHeatmap)}
            className={`px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider border flex items-center gap-1.5 transition-colors ${
              showHeatmap
                ? 'bg-[#35B8C4]/20 border-[#35B8C4] text-[#35B8C4]'
                : 'bg-[#0A0D0A] border-[#2A322C] text-[#8A968A] hover:text-[#D8E0D8]'
            }`}
          >
            <Layers className="w-3 h-3" />
            HEATMAP OVERLAY {showHeatmap ? 'ON' : 'OFF'}
          </button>
          <span className="text-[10px] text-[#8A968A]">SCALE: 100 KM</span>
        </div>
      </div>

      {/* Centerpiece Radar Canvas Viewport */}
      <div className="flex-1 flex items-center justify-center relative my-2 overflow-hidden">
        <RadarCanvas fusionResult={fusionResult} sensors={sensors} showHeatmap={showHeatmap} />
      </div>

      {/* Anchored Bottom Threat Summary & Mission Output Bar */}
      {fusionResult && (
        <div className="bg-[#141815] border border-[#2A322C] p-3 z-10 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-[#C6362F]/20 border border-[#C6362F] flex items-center justify-center rounded-[1px]">
              <ShieldAlert className="w-5 h-5 text-[#C6362F] animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-xs text-[#D8E0D8] tracking-wider uppercase">
                  {fusionResult.threatClassification}
                </span>
                <StatusChip status={fusionResult.threatLevel} size="sm" />
              </div>
              <div className="text-[10px] text-[#8A968A] flex items-center gap-2">
                <span>FUSED CONFIDENCE: <strong className="text-[#5FA85F]">{(fusionResult.fusedConfidence * 100).toFixed(1)}%</strong></span>
                <span>•</span>
                <span>ACTIVE TRACKS: <strong className="text-[#35B8C4]">{fusionResult.targetTracks.length}</strong></span>
              </div>
            </div>
          </div>

          <div className="bg-[#0A0D0A] p-2 border border-[#5FA85F] text-right font-mono max-w-md">
            <div className="text-[9px] text-[#8A968A] uppercase tracking-wider flex items-center justify-end gap-1">
              <Navigation className="w-3 h-3 text-[#5FA85F]" />
              RECOMMENDED MISSION DECISION
            </div>
            <div className="text-xs font-bold text-[#5FA85F] uppercase tracking-wide text-glow-green">
              {fusionResult.decision}
            </div>
          </div>
        </div>
      )}
    </main>
  );
};
