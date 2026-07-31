import React, { useEffect, useRef, useState } from 'react';
import type { FusionResult, SensorTelemetry, TargetTrack } from '../../types/contracts';
import { polarToCartesian } from '../../utils/polarCoordinates';
import { useMissionStore } from '../../store/missionStore';

interface RadarCanvasProps {
  fusionResult: FusionResult | null;
  sensors: SensorTelemetry[];
  maxRangeKm?: number;
  showHeatmap?: boolean;
}

export const RadarCanvas: React.FC<RadarCanvasProps> = ({
  fusionResult,
  sensors,
  maxRangeKm = 100,
  showHeatmap = false,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const selectedSensorId = useMissionStore((s) => s.selectedSensorId);
  const selectedTrackId = useMissionStore((s) => s.selectedTrackId);
  const setSelectedTrackId = useMissionStore((s) => s.setSelectedTrackId);

  const [activePopover, setActivePopover] = useState<{
    trackId: string;
    x: number;
    y: number;
    classification: string;
    confidence: number;
    range: number;
    bearing: number;
    velocity?: number;
  } | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let sweepAngle = 0;

    const render = () => {
      const size = Math.min(canvas.clientWidth, canvas.clientHeight);
      canvas.width = size;
      canvas.height = size;
      const center = size / 2;
      const radius = center - 24;

      ctx.clearRect(0, 0, size, size);

      // --- 1. Background Grid & Radar Circles ---
      ctx.strokeStyle = '#2A322C';
      ctx.lineWidth = 1;

      // Range Rings (20%, 40%, 60%, 80%, 100%)
      const ringSteps = [0.2, 0.4, 0.6, 0.8, 1.0];
      ringSteps.forEach((step) => {
        ctx.beginPath();
        ctx.arc(center, center, radius * step, 0, Math.PI * 2);
        ctx.stroke();

        // Label ring range
        ctx.fillStyle = '#8A968A';
        ctx.font = '9px "JetBrains Mono"';
        ctx.fillText(`${(step * maxRangeKm).toFixed(0)}km`, center + 4, center - radius * step + 10);
      });

      // Crosshair & Cardinal Axis
      ctx.beginPath();
      ctx.moveTo(center - radius, center);
      ctx.lineTo(center + radius, center);
      ctx.moveTo(center, center - radius);
      ctx.lineTo(center, center + radius);
      ctx.stroke();

      // Cardinal Labels (N, E, S, W)
      ctx.fillStyle = '#5FA85F';
      ctx.font = 'bold 11px "JetBrains Mono"';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('000° N', center, center - radius - 12);
      ctx.fillText('090° E', center + radius + 14, center);
      ctx.fillText('180° S', center, center + radius + 12);
      ctx.fillText('270° W', center - radius - 14, center);

      // --- 2. Heatmap Coverage Overlay (if enabled) ---
      if (showHeatmap && sensors.length > 0) {
        sensors.forEach((s) => {
          if (!s.position) return;
          const { x, y } = polarToCartesian(s.position.range, s.position.bearing, maxRangeKm, radius);
          const drawX = center + (x - radius);
          const drawY = center + (y - radius);

          const grad = ctx.createRadialGradient(drawX, drawY, 5, drawX, drawY, 60);
          grad.addColorStop(0, `rgba(53, 184, 196, ${s.confidence * 0.25})`);
          grad.addColorStop(1, 'rgba(53, 184, 196, 0)');
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(drawX, drawY, 60, 0, Math.PI * 2);
          ctx.fill();
        });
      }

      // --- 3. Sensor Locations ---
      sensors.forEach((s) => {
        if (!s.position) return;
        const { x, y } = polarToCartesian(s.position.range, s.position.bearing, maxRangeKm, radius);
        const drawX = center + (x - radius);
        const drawY = center + (y - radius);

        const isSensorSelected = selectedSensorId === s.sensorId;
        ctx.fillStyle = isSensorSelected ? '#5FA85F' : '#35B8C4';
        ctx.beginPath();
        ctx.arc(drawX, drawY, isSensorSelected ? 5 : 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#D8E0D8';
        ctx.font = '9px "JetBrains Mono"';
        ctx.textAlign = 'left';
        ctx.fillText(s.sensorId, drawX + 6, drawY + 3);
      });

      // --- 4. Rotating Sweep Line with Conic Fade ---
      sweepAngle = (sweepAngle + 0.015) % (Math.PI * 2);
      const sweepX = center + radius * Math.cos(sweepAngle);
      const sweepY = center + radius * Math.sin(sweepAngle);

      // Sweep gradient cone
      const sweepGrad = ctx.createConicGradient(sweepAngle, center, center);
      sweepGrad.addColorStop(0, 'rgba(53, 184, 196, 0.35)');
      sweepGrad.addColorStop(0.12, 'rgba(53, 184, 196, 0.05)');
      sweepGrad.addColorStop(0.25, 'rgba(53, 184, 196, 0)');
      sweepGrad.addColorStop(1, 'rgba(53, 184, 196, 0)');

      ctx.fillStyle = sweepGrad;
      ctx.beginPath();
      ctx.arc(center, center, radius, 0, Math.PI * 2);
      ctx.fill();

      // Main Sweep Ray Line
      ctx.strokeStyle = '#35B8C4';
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.moveTo(center, center);
      ctx.lineTo(sweepX, sweepY);
      ctx.stroke();

      // --- 5. Target Tracks Plotting ---
      if (fusionResult && fusionResult.targetTracks) {
        fusionResult.targetTracks.forEach((track) => {
          const { x, y } = polarToCartesian(track.range, track.bearing, maxRangeKm, radius);
          const drawX = center + (x - radius);
          const drawY = center + (y - radius);

          const isTrackSelected = selectedTrackId === track.trackId;

          // Target color by threat confidence/classification
          const targetColor =
            fusionResult.threatLevel === 'critical' ? '#C6362F' :
            fusionResult.threatLevel === 'high' ? '#D99A2B' : '#5FA85F';

          // Fading track trail line
          ctx.strokeStyle = `${targetColor}66`;
          ctx.lineWidth = 1;
          ctx.setLineDash([2, 2]);
          ctx.beginPath();
          ctx.moveTo(drawX - 12, drawY + 8);
          ctx.lineTo(drawX, drawY);
          ctx.stroke();
          ctx.setLineDash([]);

          // Marker Symbol (Diamond/Box)
          ctx.strokeStyle = targetColor;
          ctx.lineWidth = isTrackSelected ? 2.5 : 1.5;
          ctx.strokeRect(drawX - 6, drawY - 6, 12, 12);

          if (isTrackSelected) {
            ctx.strokeStyle = '#FFFFFF';
            ctx.strokeRect(drawX - 8, drawY - 8, 16, 16);
          }

          // Target Label
          ctx.fillStyle = '#D8E0D8';
          ctx.font = 'bold 9px "JetBrains Mono"';
          ctx.textAlign = 'left';
          ctx.fillText(track.trackId, drawX + 9, drawY - 2);

          ctx.fillStyle = targetColor;
          ctx.font = '8px "JetBrains Mono"';
          ctx.fillText(`${(track.confidence * 100).toFixed(0)}% RCS LOCK`, drawX + 9, drawY + 8);
        });
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [fusionResult, sensors, maxRangeKm, showHeatmap, selectedSensorId, selectedTrackId]);

  // Click handler on canvas to open target track popover
  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas || !fusionResult) return;
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    const size = Math.min(canvas.clientWidth, canvas.clientHeight);
    const center = size / 2;
    const radius = center - 24;

    let clickedTrack: (TargetTrack & { x: number; y: number }) | null = null;
    for (const tr of fusionResult.targetTracks) {
      const { x, y } = polarToCartesian(tr.range, tr.bearing, maxRangeKm, radius);
      const drawX = center + (x - radius);
      const drawY = center + (y - radius);
      const dist = Math.hypot(clickX - drawX, clickY - drawY);
      if (dist <= 15) {
        clickedTrack = { ...tr, x: drawX, y: drawY };
        break;
      }
    }

    if (clickedTrack) {
      setSelectedTrackId(clickedTrack.trackId);
      setActivePopover(clickedTrack);
    } else {
      setSelectedTrackId(null);
      setActivePopover(null);
    }
  };

  return (
    <div className="relative w-full h-full flex items-center justify-center bg-[#0A0D0A]">
      <canvas
        ref={canvasRef}
        onClick={handleCanvasClick}
        className="w-full h-full max-w-[580px] max-h-[580px] block cursor-pointer"
      />

      {/* Target Detail Popover on Click */}
      {activePopover && (
        <div
          className="absolute z-30 c2-card p-3 w-56 border-[#35B8C4] text-[10px] space-y-1 shadow-2xl animate-in fade-in zoom-in-95 duration-150"
          style={{
            top: `${Math.min(activePopover.y, 400)}px`,
            left: `${Math.min(activePopover.x + 10, 360)}px`,
          }}
        >
          <div className="flex justify-between items-center border-b border-[#2A322C] pb-1 font-bold text-[#35B8C4]">
            <span>{activePopover.trackId}</span>
            <button
              onClick={() => setActivePopover(null)}
              className="text-[#8A968A] hover:text-[#D8E0D8] text-xs font-mono"
            >
              ✕
            </button>
          </div>
          <div className="text-[#D8E0D8] font-semibold">{activePopover.classification}</div>
          <div className="grid grid-cols-2 gap-1 text-[#8A968A]">
            <div>RANGE: <span className="text-[#D8E0D8]">{activePopover.range.toFixed(1)} km</span></div>
            <div>BEARING: <span className="text-[#D8E0D8]">{activePopover.bearing.toFixed(1)}°</span></div>
            <div>VELOCITY: <span className="text-[#D8E0D8]">{activePopover.velocity ?? 520} km/h</span></div>
            <div>CONFIDENCE: <span className="text-[#5FA85F]">{(activePopover.confidence * 100).toFixed(1)}%</span></div>
          </div>
        </div>
      )}
    </div>
  );
};
