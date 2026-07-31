import React from 'react';
import { clsx } from 'clsx';
import { Radio, ShieldAlert, Cpu, Activity, Camera } from 'lucide-react';
import type { SensorTelemetry } from '../../types/contracts';
import { StatusChip } from '../common/StatusChip';
import { Gauge } from '../common/Gauge';
import { SensorWaveform } from './SensorWaveform';
import { formatShortTimestamp } from '../../utils/formatters';
import { useMissionStore } from '../../store/missionStore';

interface SensorCardProps {
  sensor: SensorTelemetry;
}

export const SensorCard: React.FC<SensorCardProps> = ({ sensor }) => {
  const selectedSensorId = useMissionStore((s) => s.selectedSensorId);
  const setSelectedSensorId = useMissionStore((s) => s.setSelectedSensorId);

  const isSelected = selectedSensorId === sensor.sensorId;

  // Generic icon resolution - fallback icon if unknown type (Section 12 requirement)
  const getSensorIcon = (type: string) => {
    const t = type.toLowerCase();
    if (t.includes('radar')) return Radio;
    if (t.includes('infra') || t.includes('therm')) return ShieldAlert;
    if (t.includes('acoust')) return Activity;
    if (t.includes('camera') || t.includes('eo')) return Camera;
    return Cpu; // generic default icon
  };

  const IconComponent = getSensorIcon(sensor.sensorType);

  const waveformColor =
    sensor.status === 'online' ? '#5FA85F' :
    sensor.status === 'degraded' ? '#D99A2B' : '#4A4A4A';

  return (
    <div
      onClick={() => setSelectedSensorId(isSelected ? null : sensor.sensorId)}
      className={clsx(
        'c2-card p-3 cursor-pointer transition-all duration-200 space-y-2 hover:border-[#5FA85F]/60',
        isSelected && 'c2-card-glow border-[#5FA85F] bg-[#141815]'
      )}
    >
      {/* Top Header: Icon + Sensor ID + Type + Status */}
      <div className="flex items-center justify-between border-b border-[#2A322C] pb-1.5">
        <div className="flex items-center gap-2">
          <IconComponent className={clsx('w-4 h-4', isSelected ? 'text-[#5FA85F]' : 'text-[#35B8C4]')} />
          <div>
            <div className="font-bold text-[12px] tracking-wider text-[#D8E0D8] uppercase">{sensor.sensorId}</div>
            <div className="text-[9px] text-[#8A968A] uppercase tracking-widest">{sensor.sensorType}</div>
          </div>
        </div>
        <StatusChip status={sensor.status} size="sm" />
      </div>

      {/* Gauges Grid */}
      <div className="grid grid-cols-2 gap-x-3 gap-y-1.5 py-1">
        <Gauge label="Confidence" value={sensor.confidence} />
        <Gauge label="Reliability" value={sensor.reliability} />
        <Gauge label="Noise Level" value={sensor.noise} warningThreshold={0.5} criticalThreshold={0.8} />
        <Gauge label="Signal Quality" value={sensor.signalQuality} />
      </div>

      {/* Waveform Strip */}
      <div className="space-y-1">
        <div className="flex justify-between text-[9px] text-[#8A968A] uppercase tracking-wider">
          <span>Signal Buffer</span>
          <span>Health: {(sensor.health * 100).toFixed(0)}%</span>
        </div>
        <SensorWaveform waveform={sensor.waveform} color={waveformColor} height={22} />
      </div>

      {/* Footer Timestamp */}
      <div className="text-[9px] text-[#8A968A] text-right font-mono tracking-wider pt-0.5">
        UPDATED: {formatShortTimestamp(sensor.lastUpdated)}
      </div>
    </div>
  );
};
