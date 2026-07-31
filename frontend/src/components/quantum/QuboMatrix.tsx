import React, { useState } from 'react';
import type { QuantumEngineResult } from '../../types/contracts';
import { clsx } from 'clsx';

interface QuboMatrixProps {
  quantumResult: QuantumEngineResult | null;
}

export const QuboMatrix: React.FC<QuboMatrixProps> = ({ quantumResult }) => {
  const [hoveredCell, setHoveredCell] = useState<{ row: number; col: number; val: number } | null>(null);

  if (!quantumResult || !quantumResult.quboMatrix || quantumResult.quboMatrix.length === 0) {
    return (
      <div className="c2-card p-3 text-[11px] text-[#8A968A]">
        AWAITING QUBO MATRIX FORMULATION...
      </div>
    );
  }

  const matrix = quantumResult.quboMatrix;
  const n = matrix.length;

  // Compute max absolute value for heat color scaling
  let maxAbs = 0.001;
  matrix.forEach((row) =>
    row.forEach((val) => {
      if (Math.abs(val) > maxAbs) maxAbs = Math.abs(val);
    })
  );

  return (
    <div className="c2-card p-3 space-y-2 font-mono">
      <div className="flex justify-between items-center border-b border-[#2A322C] pb-1 text-[11px]">
        <span className="font-bold text-[#D8E0D8] uppercase tracking-wider">QUBO MATRIX ({n}x{n})</span>
        <span className="text-[10px] text-[#35B8C4]">ISING / QUBO SOLVER</span>
      </div>

      {/* Heatmap Grid */}
      <div className="overflow-x-auto py-1">
        <div className="inline-block min-w-full">
          <div
            className="grid gap-[2px] bg-[#0A0D0A] p-[2px] border border-[#2A322C]"
            style={{ gridTemplateColumns: `repeat(${n}, minmax(36px, 1fr))` }}
          >
            {matrix.map((row, rIdx) =>
              row.map((val, cIdx) => {
                const isHovered = hoveredCell?.row === rIdx || hoveredCell?.col === cIdx;
                const isExact = hoveredCell?.row === rIdx && hoveredCell?.col === cIdx;

                // Energy color scaling: negative values cyan/green, positive values amber/red
                const intensity = Math.min(1, Math.abs(val) / maxAbs);
                const bgStyle =
                  val < 0
                    ? `rgba(53, 184, 196, ${0.15 + intensity * 0.65})`
                    : `rgba(217, 154, 43, ${0.15 + intensity * 0.65})`;

                return (
                  <div
                    key={`${rIdx}-${cIdx}`}
                    onMouseEnter={() => setHoveredCell({ row: rIdx, col: cIdx, val })}
                    onMouseLeave={() => setHoveredCell(null)}
                    style={{ backgroundColor: bgStyle }}
                    className={clsx(
                      'h-8 flex items-center justify-center text-[10px] cursor-pointer transition-all duration-150 rounded-[1px]',
                      isExact ? 'border border-[#FFFFFF] shadow-lg z-10 font-bold scale-105' :
                      isHovered ? 'border border-[#5FA85F] text-[#FFFFFF]' : 'border border-transparent text-[#D8E0D8]'
                    )}
                  >
                    {val.toFixed(2)}
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* Cell Hover Readout Footer */}
      <div className="flex justify-between items-center text-[10px] text-[#8A968A] pt-0.5 border-t border-[#2A322C]">
        <div>
          {hoveredCell ? (
            <span>
              CELL Q[{hoveredCell.row}][{hoveredCell.col}] = <span className="font-bold text-[#5FA85F]">{hoveredCell.val.toFixed(3)}</span>
            </span>
          ) : (
            <span>HOVER MATRIX CELLS TO INSPECT INTERACTION COEFFS</span>
          )}
        </div>
        <div className="flex items-center gap-2 text-[9px]">
          <span className="flex items-center gap-1"><span className="w-2 h-2 bg-[#35B8C4] inline-block" /> NEG (FAVORABLE)</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 bg-[#D99A2B] inline-block" /> POS (PENALTY)</span>
        </div>
      </div>
    </div>
  );
};
