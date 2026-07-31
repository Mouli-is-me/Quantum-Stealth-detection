import React from 'react';
import { useReplayStore } from '../../store/replayStore';
import { Play, Pause, SkipBack, SkipForward, RotateCcw } from 'lucide-react';
import { formatShortTimestamp } from '../../utils/formatters';

export const ReplayScrubber: React.FC = () => {
  const isReplayActive = useReplayStore((s) => s.isReplayActive);
  const replayFrames = useReplayStore((s) => s.replayFrames);
  const currentFrameIndex = useReplayStore((s) => s.currentFrameIndex);
  const isPlaying = useReplayStore((s) => s.isPlaying);
  const playbackSpeed = useReplayStore((s) => s.playbackSpeed);

  const setReplayActive = useReplayStore((s) => s.setReplayActive);
  const setCurrentFrameIndex = useReplayStore((s) => s.setCurrentFrameIndex);
  const setIsPlaying = useReplayStore((s) => s.setIsPlaying);
  const setPlaybackSpeed = useReplayStore((s) => s.setPlaybackSpeed);

  const currentFrame = replayFrames[currentFrameIndex];
  const maxIndex = Math.max(0, replayFrames.length - 1);

  return (
    <div className="c2-card p-4 space-y-3 font-mono border-t-2 border-t-[#35B8C4]">
      {/* Banner */}
      <div className="flex justify-between items-center border-b border-[#2A322C] pb-2">
        <div>
          <div className="text-sm font-bold text-[#35B8C4] uppercase tracking-wider text-glow-cyan flex items-center gap-2">
            <span>MISSION REPLAY & TIMELINE SCRUBBER</span>
            {isReplayActive && (
              <span className="px-2 py-0.5 bg-[#D99A2B]/20 border border-[#D99A2B] text-[#D99A2B] text-[10px]">
                REPLAY MODE ACTIVE
              </span>
            )}
          </div>
          <div className="text-[10px] text-[#8A968A]">
            {replayFrames.length} buffered tactical frames available in ring buffer.
          </div>
        </div>

        <button
          onClick={() => setReplayActive(!isReplayActive)}
          className={`px-3 py-1 text-xs font-bold uppercase tracking-wider border rounded-[1px] transition-all ${
            isReplayActive
              ? 'bg-[#D99A2B]/20 border-[#D99A2B] text-[#D99A2B] hover:bg-[#D99A2B]/40'
              : 'bg-[#3F6B3F]/20 border-[#5FA85F] text-[#5FA85F] hover:bg-[#3F6B3F]/40'
          }`}
        >
          {isReplayActive ? 'EXIT REPLAY MODE' : 'ENTER REPLAY MODE'}
        </button>
      </div>

      {/* Scrub Controls & Timeline */}
      <div className="space-y-2 pt-1">
        {/* Scrubber Slider */}
        <div className="flex items-center gap-3">
          <span className="text-[10px] text-[#8A968A]">FRAME {currentFrameIndex + 1}/{replayFrames.length || 1}</span>
          <input
            type="range"
            min={0}
            max={maxIndex}
            value={currentFrameIndex}
            disabled={!isReplayActive || replayFrames.length === 0}
            onChange={(e) => setCurrentFrameIndex(parseInt(e.target.value))}
            className="flex-1 accent-[#35B8C4] bg-[#0A0D0A] cursor-pointer"
          />
          <span className="text-[10px] font-bold text-[#D8E0D8]">
            {currentFrame ? formatShortTimestamp(currentFrame.timestamp) : 'N/A'}
          </span>
        </div>

        {/* Playback Buttons */}
        <div className="flex items-center justify-between bg-[#0A0D0A] p-2 border border-[#2A322C]">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentFrameIndex(0)}
              disabled={!isReplayActive}
              className="p-1 hover:bg-[#2A322C] text-[#D8E0D8] border border-[#2A322C] disabled:opacity-40"
              title="Reset to Start"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={() => setCurrentFrameIndex(Math.max(0, currentFrameIndex - 1))}
              disabled={!isReplayActive || currentFrameIndex === 0}
              className="p-1 hover:bg-[#2A322C] text-[#D8E0D8] border border-[#2A322C] disabled:opacity-40"
              title="Step Back"
            >
              <SkipBack className="w-4 h-4" />
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              disabled={!isReplayActive}
              className="px-3 py-1 bg-[#35B8C4]/20 border border-[#35B8C4] text-[#35B8C4] hover:bg-[#35B8C4]/40 font-bold text-xs flex items-center gap-1.5 disabled:opacity-40"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {isPlaying ? 'PAUSE' : 'PLAY'}
            </button>
            <button
              onClick={() => setCurrentFrameIndex(Math.min(maxIndex, currentFrameIndex + 1))}
              disabled={!isReplayActive || currentFrameIndex === maxIndex}
              className="p-1 hover:bg-[#2A322C] text-[#D8E0D8] border border-[#2A322C] disabled:opacity-40"
              title="Step Forward"
            >
              <SkipForward className="w-4 h-4" />
            </button>
          </div>

          {/* Speed Select */}
          <div className="flex items-center gap-2 text-[10px]">
            <span className="text-[#8A968A]">SPEED:</span>
            {[0.5, 1.0, 2.0, 4.0].map((spd) => (
              <button
                key={spd}
                onClick={() => setPlaybackSpeed(spd)}
                className={`px-2 py-0.5 border text-[10px] font-bold ${
                  playbackSpeed === spd
                    ? 'bg-[#35B8C4] text-[#0A0D0A] border-[#35B8C4]'
                    : 'bg-[#141815] text-[#8A968A] border-[#2A322C] hover:text-[#D8E0D8]'
                }`}
              >
                {spd}x
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
