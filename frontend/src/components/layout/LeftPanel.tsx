import React from 'react';
import { useSensorStore } from '../../store/sensorStore';
import { useMissionStore } from '../../store/missionStore';
import { SensorCard } from '../sensors/SensorCard';
import { LoadingSkeleton } from '../common/LoadingSkeleton';
import { ErrorBanner } from '../common/ErrorBanner';
import { EmptyState } from '../common/EmptyState';
import { Radio } from 'lucide-react';

export const LeftPanel: React.FC = () => {
  const sensors = useSensorStore((s) => s.sensors);
  const dataState = useSensorStore((s) => s.dataState);
  const errorMessage = useMissionStore((s) => s.errorMessage);

  return (
    <aside className="w-80 h-full bg-[#141815] border-r border-[#2A322C] flex flex-col font-mono select-none overflow-hidden shrink-0">
      {/* Panel Header */}
      <div className="p-3 border-b border-[#2A322C] flex justify-between items-center bg-[#0A0D0A]">
        <div className="flex items-center gap-2">
          <Radio className="w-4 h-4 text-[#35B8C4]" />
          <span className="font-bold text-xs tracking-wider text-[#D8E0D8] uppercase">
            LIVE SENSOR TELEMETRY
          </span>
        </div>
        <span className="px-2 py-0.5 bg-[#141815] border border-[#2A322C] text-[#35B8C4] text-[10px] font-bold">
          {sensors.length} ACTIVE
        </span>
      </div>

      {/* Sensor List Scroll Container */}
      <div className="flex-1 p-3 overflow-y-auto space-y-3">
        {dataState === 'loading' && sensors.length === 0 ? (
          <LoadingSkeleton label="INITIALIZING SENSOR BUS..." />
        ) : dataState === 'error' ? (
          <ErrorBanner message={errorMessage || 'Sensor telemetry failure'} />
        ) : sensors.length === 0 ? (
          <EmptyState />
        ) : (
          sensors.map((sensor) => (
            <SensorCard key={sensor.sensorId} sensor={sensor} />
          ))
        )}
      </div>

      {/* Footer Info */}
      <div className="p-2 border-t border-[#2A322C] bg-[#0A0D0A] text-[9px] text-[#8A968A] text-center uppercase tracking-wider">
        SELECT CARD TO CROSS-HIGHLIGHT ON RADAR
      </div>
    </aside>
  );
};
