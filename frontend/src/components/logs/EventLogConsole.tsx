import React, { useRef, useEffect } from 'react';
import { useLogStore } from '../../store/logStore';
import { formatShortTimestamp } from '../../utils/formatters';
import { clsx } from 'clsx';
import { Terminal, Trash2 } from 'lucide-react';

export const EventLogConsole: React.FC = () => {
  const logs = useLogStore((s) => s.logs);
  const filterStage = useLogStore((s) => s.filterStage);
  const filterSeverity = useLogStore((s) => s.filterSeverity);
  const setFilterStage = useLogStore((s) => s.setFilterStage);
  const setFilterSeverity = useLogStore((s) => s.setFilterSeverity);
  const clearLogs = useLogStore((s) => s.clearLogs);

  const consoleEndRef = useRef<HTMLDivElement | null>(null);

  const filteredLogs = logs.filter((log) => {
    if (filterStage !== 'all' && log.stage !== filterStage) return false;
    if (filterSeverity !== 'all' && log.severity !== filterSeverity) return false;
    return true;
  });

  useEffect(() => {
    consoleEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [filteredLogs]);

  const getSeverityStyle = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-[#C6362F] font-bold text-glow-red';
      case 'warning':
        return 'text-[#D99A2B] font-semibold';
      case 'info':
      default:
        return 'text-[#D8E0D8]';
    }
  };

  return (
    <div className="c2-card p-3 space-y-2 font-mono flex flex-col h-full min-h-[300px]">
      {/* Console Toolbar Controls */}
      <div className="flex justify-between items-center border-b border-[#2A322C] pb-2 text-[11px]">
        <div className="flex items-center gap-2 font-bold text-[#D8E0D8] uppercase tracking-wider">
          <Terminal className="w-4 h-4 text-[#35B8C4]" />
          <span>MILITARY C2 EVENT CONSOLE</span>
          <span className="text-[9px] text-[#8A968A]">({filteredLogs.length} EVENTS)</span>
        </div>

        {/* Filter selects */}
        <div className="flex items-center gap-2">
          <select
            value={filterStage}
            onChange={(e: any) => setFilterStage(e.target.value)}
            className="bg-[#0A0D0A] border border-[#2A322C] text-[#8A968A] text-[10px] px-2 py-0.5 uppercase rounded-[1px] focus:outline-none focus:border-[#5FA85F]"
          >
            <option value="all">ALL STAGES</option>
            <option value="sensor">SENSOR</option>
            <option value="ai">AI</option>
            <option value="quantum">QUANTUM</option>
            <option value="classical">CLASSICAL</option>
            <option value="fusion">FUSION</option>
            <option value="system">SYSTEM</option>
          </select>

          <select
            value={filterSeverity}
            onChange={(e: any) => setFilterSeverity(e.target.value)}
            className="bg-[#0A0D0A] border border-[#2A322C] text-[#8A968A] text-[10px] px-2 py-0.5 uppercase rounded-[1px] focus:outline-none focus:border-[#5FA85F]"
          >
            <option value="all">ALL SEVERITY</option>
            <option value="info">INFO</option>
            <option value="warning">WARNING</option>
            <option value="critical">CRITICAL</option>
          </select>

          <button
            onClick={clearLogs}
            className="p-1 hover:bg-[#C6362F]/20 text-[#8A968A] hover:text-[#C6362F] border border-[#2A322C] transition-colors rounded-[1px]"
            title="Clear Console"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Log Output Stream */}
      <div className="flex-1 bg-[#0A0D0A] border border-[#2A322C] p-2 overflow-y-auto space-y-1 text-[11px] select-text max-h-[360px]">
        <div className="text-[9px] text-[#8A968A] border-b border-[#2A322C] pb-1 mb-1 font-mono uppercase tracking-widest">
          [TIME] [STAGE] [SEVERITY] MESSAGE (NEWEST AT BOTTOM)
        </div>
        {filteredLogs.length === 0 ? (
          <div className="text-[#8A968A] text-center py-6">NO LOG EVENTS MATCHING CURRENT FILTERS</div>
        ) : (
          filteredLogs.map((log) => (
            <div key={log.id} className="flex gap-2 items-start hover:bg-[#141815] py-0.5 px-1">
              <span className="text-[#8A968A] shrink-0 font-mono text-[10px]">{formatShortTimestamp(log.timestamp)}</span>
              <span className="px-1 bg-[#1A201C] border border-[#2A322C] text-[#35B8C4] text-[9px] uppercase font-bold shrink-0">
                {log.stage}
              </span>
              <span className={clsx('uppercase text-[9px] font-bold shrink-0 w-14', getSeverityStyle(log.severity))}>
                [{log.severity}]
              </span>
              <span className={clsx('flex-1 font-mono text-[11px] leading-snug', getSeverityStyle(log.severity))}>
                {log.message}
              </span>
            </div>
          ))
        )}
        <div ref={consoleEndRef} />
      </div>
    </div>
  );
};
