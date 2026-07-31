/**
 * Formatting utilities for C2 dashboard telemetry
 */

export function formatPercent(value: number): string {
  const pct = value > 1 ? value : value * 100;
  return `${pct.toFixed(1)}%`;
}

export function formatEnergy(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(4)} eV`;
}

export function formatMs(ms: number): string {
  return `${ms.toFixed(2)} ms`;
}

export function formatNibbles(bitstring: string): string {
  if (!bitstring) return '0000';
  return bitstring.match(/.{1,4}/g)?.join(' ') || bitstring;
}

export function formatIsoTime(isoString: string): string {
  try {
    const d = new Date(isoString);
    const hours = String(d.getHours()).padStart(2, '0');
    const mins = String(d.getMinutes()).padStart(2, '0');
    const secs = String(d.getSeconds()).padStart(2, '0');
    const ms = String(d.getMilliseconds()).padStart(3, '0');
    return `${hours}:${mins}:${secs}.${ms}`;
  } catch {
    return isoString;
  }
}

export function formatShortTimestamp(isoString: string): string {
  try {
    const d = new Date(isoString);
    return d.toTimeString().split(' ')[0];
  } catch {
    return isoString;
  }
}
