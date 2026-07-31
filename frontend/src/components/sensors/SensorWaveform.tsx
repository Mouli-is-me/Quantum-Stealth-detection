import React, { useEffect, useRef } from 'react';

interface SensorWaveformProps {
  waveform: number[];
  color?: string;
  height?: number;
}

export const SensorWaveform: React.FC<SensorWaveformProps> = ({
  waveform = [],
  color = '#5FA85F',
  height = 24,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.clientWidth;
    const canvasHeight = canvas.clientHeight;
    canvas.width = width;
    canvas.height = canvasHeight;

    ctx.clearRect(0, 0, width, canvasHeight);

    if (waveform.length === 0) {
      // Flat line fallback
      ctx.strokeStyle = '#4A4A4A';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, canvasHeight / 2);
      ctx.lineTo(width, canvasHeight / 2);
      ctx.stroke();
      return;
    }

    const step = width / Math.max(1, waveform.length - 1);
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.beginPath();

    waveform.forEach((val, idx) => {
      const x = idx * step;
      // Map val (typically 0..1 or -1..1) to canvas height
      const normalized = Math.max(-1, Math.min(1, val));
      const y = canvasHeight / 2 - (normalized * (canvasHeight / 2 - 2));
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });

    ctx.stroke();

    // Subtle glow under waveform
    ctx.shadowColor = color;
    ctx.shadowBlur = 4;
  }, [waveform, color, height]);

  return (
    <div className="w-full bg-[#0A0D0A] border border-[#2A322C] rounded-[1px] p-[1px]">
      <canvas
        ref={canvasRef}
        className="w-full block"
        style={{ height: `${height}px` }}
      />
    </div>
  );
};
