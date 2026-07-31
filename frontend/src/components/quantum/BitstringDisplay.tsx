import React from 'react';
import type { QuantumEngineResult } from '../../types/contracts';
import { formatEnergy, formatNibbles, formatMs } from '../../utils/formatters';
import { Zap, Clock, Cpu } from 'lucide-react';

interface BitstringDisplayProps {
  quantumResult: QuantumEngineResult | null;
}

export const BitstringDisplay: React.FC<BitstringDisplayProps> = ({ quantumResult }) => {
  if (!quantumResult) return null;

  return (
    <div className="c2-card p-3 space-y-2.5 font-mono">
      {/* Top Banner: Lowest Energy & Execution Time */}
      <div className="grid grid-cols-2 gap-2">
        <div className="bg-[#0A0D0A] p-2 border border-[#5FA85F] space-y-0.5">
          <div className="flex items-center gap-1 text-[9px] text-[#8A968A] uppercase tracking-wider">
            <Zap className="w-3 h-3 text-[#5FA85F]" />
            <span>LOWEST GROUND ENERGY</span>
          </div>
          <div className="text-base font-bold text-[#5FA85F] text-glow-green">
            {formatEnergy(quantumResult.lowestEnergy)}
          </div>
        </div>

        <div className="bg-[#0A0D0A] p-2 border border-[#2A322C] space-y-0.5">
          <div className="flex items-center gap-1 text-[9px] text-[#8A968A] uppercase tracking-wider">
            <Clock className="w-3 h-3 text-[#35B8C4]" />
            <span>QPU LATENCY</span>
          </div>
          <div className="text-base font-bold text-[#35B8C4]">
            {formatMs(quantumResult.executionTimeMs)}
          </div>
        </div>
      </div>

      {/* Bitstring Grouped in Nibbles */}
      <div className="bg-[#0A0D0A] p-2 border border-[#2A322C] space-y-1">
        <div className="flex justify-between items-center text-[9px] text-[#8A968A] uppercase tracking-wider">
          <span>OPTIONAL SENSOR BITSTRING</span>
          <span className="text-[#D8E0D8]">{quantumResult.selectedSensors.length} ACTIVE BITS</span>
        </div>
        <div className="text-lg font-bold text-[#D8E0D8] tracking-widest text-center py-1 bg-[#141815] border border-[#2A322C]">
          {formatNibbles(quantumResult.bitstring)}
        </div>
      </div>

      {/* Selected Sensors Chips */}
      <div className="space-y-1">
        <div className="text-[9px] text-[#8A968A] uppercase tracking-wider flex items-center gap-1">
          <Cpu className="w-3 h-3 text-[#5FA85F]" />
          <span>QUANTUM OPTIMIZED SENSOR SUBSET</span>
        </div>
        <div className="flex flex-wrap gap-1.5 pt-0.5">
          {quantumResult.selectedSensors.map((sensorId) => (
            <span
              key={sensorId}
              className="px-2 py-0.5 bg-[#3F6B3F]/20 border border-[#5FA85F] text-[#5FA85F] text-[10px] font-bold tracking-wider uppercase rounded-[1px]"
            >
              ✓ {sensorId}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};
