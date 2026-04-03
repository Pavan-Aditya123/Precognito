/**
 * @file SensorRow component for displaying an individual sensor's status in a table row.
 */

"use client";

import { SensorStatus } from "@/lib/types";

interface SensorRowProps {
  sensor: SensorStatus;
}

const statusConfig: Record<SensorStatus["status"], { color: string; bg: string; label: string }> = {
  ONLINE: { color: "text-white", bg: "bg-[#22c55e]", label: "Online" },
  DEGRADED: { color: "text-black", bg: "bg-[#eab308]", label: "Degraded" },
  OFFLINE: { color: "text-white", bg: "bg-[#ef4444]", label: "Offline" },
};

/**
 * Formats a ISO timestamp into a relative time string (e.g., "5 min ago").
 * 
 * @param {string} timestamp The ISO timestamp string.
 * @returns {string} The formatted relative time string.
 */
function formatTimeAgo(timestamp: string): string {
  const now = new Date();
  const sensorTime = new Date(timestamp);
  const diffMs = now.getTime() - sensorTime.getTime();
  const diffMins = Math.floor(diffMs / 60000);

  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins} min ago`;
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours} hr ago`;
  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays} day${diffDays > 1 ? "s" : ""} ago`;
}

/**
 * Gets the CSS color class based on battery level.
 * 
 * @param {number} level The battery level percentage (0-100).
 * @returns {string} The CSS class for the battery color.
 */
function getBatteryColor(level: number): string {
  if (level > 50) return "bg-[#22c55e]";
  if (level > 20) return "bg-[#eab308]";
  return "bg-[#ef4444]";
}

/**
 * Renders a table row for a single sensor.
 * 
 * @param {SensorRowProps} props The component props.
 * @param {SensorStatus} props.sensor The sensor data to display.
 * @returns {JSX.Element} The rendered sensor row.
 */
export function SensorRow({ sensor }: SensorRowProps) {
  const config = statusConfig[sensor.status];

  return (
    <tr className="border-b border-[#334155] hover:bg-[#334155] transition-colors">
      <td className="py-3 px-4">
        <div>
          <p className="text-sm font-medium text-[#f1f5f9]">{sensor.name}</p>
          <p className="text-xs text-[#64748b]">{sensor.sensorId}</p>
        </div>
      </td>
      <td className="py-3 px-4">
        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${config.bg} ${config.color}`}>
          {config.label}
        </span>
      </td>
      <td className="py-3 px-4">
        <div className="flex items-center gap-2">
          <div className="w-16 h-2 bg-[#334155] rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${getBatteryColor(sensor.batteryLevel)}`}
              style={{ width: `${sensor.batteryLevel}%` }}
            />
          </div>
          <span className="text-sm text-[#94a3b8]">{sensor.batteryLevel}%</span>
        </div>
      </td>
      <td className="py-3 px-4 text-sm text-[#94a3b8]">
        {formatTimeAgo(sensor.lastHeartbeat)}
      </td>
    </tr>
  );
}
