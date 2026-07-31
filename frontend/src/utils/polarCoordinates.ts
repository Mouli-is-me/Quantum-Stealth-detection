/**
 * Converts polar coordinates (range in km, bearing in degrees 0-360)
 * to Cartesian (x, y) coordinates relative to a circle of radius maxRadius.
 *
 * @param range Distance in km
 * @param bearing Bearing in degrees (0 = North/Top, 90 = East/Right)
 * @param maxRange Maximum range scale of the radar display (e.g. 100 km)
 * @param canvasRadius Radius of the radar display canvas in pixels
 */
export function polarToCartesian(
  range: number,
  bearing: number,
  maxRange: number,
  canvasRadius: number
): { x: number; y: number } {
  // Clamp range to maxRange
  const normalizedRange = Math.min(range / maxRange, 1.0);
  const r = normalizedRange * canvasRadius;

  // Convert bearing (0 deg = 12 o'clock / North, clockwise) to math angle in radians (0 rad = 3 o'clock)
  const angleRad = ((bearing - 90) * Math.PI) / 180;

  const x = canvasRadius + r * Math.cos(angleRad);
  const y = canvasRadius + r * Math.sin(angleRad);

  return { x, y };
}
