import React from 'react';
import type { QuantumEngineResult } from '../../types/contracts';
import { Gauge } from '../common/Gauge';

interface SensorWeightsListProps {
  quantumResult: QuantumEngineResult | null;
}

export const SensorWeightsList: React.FC<SensorWeightsListProps> = ({ quantumResult }) => {
  if (!quantumResult || !quantumResult.adaptiveSensorWeights) return null;

  const weights = Object.entries(quantumResult.adaptiveSensorWeights);

  return (
    <div className="c2-card p-3 space-y-2 font-mono">
      <div className="flex justify-between items-center border-b border-[#2A322C] pb-1 text-[11px] font-bold text-[#D8E0D8] uppercase tracking-wider">
        <span>QUANTUM ADAPTIVE SENSOR WEIGHTS</span>
        <span className="text-[10px] text-[#5FA85F]">FUSION WEIGHT COEFFS</span>
      </div>

      <div className="space-y-1.5 pt-0.5">
        {weights.map(([sensorId, weight]) => (
          <Gauge
            key={sensorId}
            label={sensorId}
            value={weight}
            showPercentage
          />
        ))}
      </div>
    </div>
  );
};
