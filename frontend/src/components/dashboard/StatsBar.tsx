/**
 * @file StatsBar component for displaying high-level asset health statistics.
 */

interface StatsBarProps {
  total: number;
  healthy: number;
  warning: number;
  critical: number;
}

/**
 * Displays a row of statistics showing total assets and counts by health status.
 * 
 * @param {StatsBarProps} props The component props.
 * @param {number} props.total Total number of assets.
 * @param {number} props.healthy Number of healthy assets.
 * @param {number} props.warning Number of assets with warnings.
 * @param {number} props.critical Number of critical assets.
 * @returns {JSX.Element} The rendered statistics bar.
 */
export function StatsBar({ total, healthy, warning, critical }: StatsBarProps) {
  return (
    <div className="flex gap-6 mb-6">
      <div className="flex items-center gap-2">
        <span className="text-2xl font-semibold text-[#f1f5f9]">{total}</span>
        <span className="text-sm text-[#94a3b8]">Total</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="w-3 h-3 rounded-full bg-[#22c55e]" />
        <span className="text-lg font-medium text-[#f1f5f9]">{healthy}</span>
        <span className="text-sm text-[#94a3b8]">Healthy</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="w-3 h-3 rounded-full bg-[#eab308]" />
        <span className="text-lg font-medium text-[#f1f5f9]">{warning}</span>
        <span className="text-sm text-[#94a3b8]">Warning</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="w-3 h-3 rounded-full bg-[#ef4444]" />
        <span className="text-lg font-medium text-[#f1f5f9]">{critical}</span>
        <span className="text-sm text-[#94a3b8]">Critical</span>
      </div>
    </div>
  );
}
