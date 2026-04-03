/**
 * @file SensorTable component for displaying a list of sensors and their statuses.
 */

"use client";

import { SensorStatus } from "@/lib/types";
import { SensorRow } from "./SensorRow";

interface SensorTableProps {
  sensors: SensorStatus[];
}

/**
 * Renders a table of sensors with a summary of their online/offline status.
 * 
 * @param {SensorTableProps} props The component props.
 * @param {SensorStatus[]} props.sensors Array of sensors to display.
 * @returns {JSX.Element} The rendered sensor table.
 */
export function SensorTable({ sensors }: SensorTableProps) {
  /**
   * Gets the count of sensors with a specific status.
   * 
   * @param {SensorStatus["status"] | "ALL"} status The status to count.
   * @returns {number} The count of sensors.
   */
  const getStatusCount = (status: SensorStatus["status"] | "ALL") => {
    if (status === "ALL") return sensors.length;
    return sensors.filter((s) => s.status === status).length;
  };

  return (
    <div>
      <div className="flex gap-4 mb-4">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-[#22c55e]" />
          <span className="text-sm text-[#94a3b8]">Online: {getStatusCount("ONLINE")}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-[#eab308]" />
          <span className="text-sm text-[#94a3b8]">Degraded: {getStatusCount("DEGRADED")}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-[#ef4444]" />
          <span className="text-sm text-[#94a3b8]">Offline: {getStatusCount("OFFLINE")}</span>
        </div>
      </div>

      <div className="border border-[#334155] rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-[#1e293b]">
            <tr>
              <th className="text-left py-3 px-4 text-sm font-medium text-[#94a3b8]">Sensor</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-[#94a3b8]">Status</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-[#94a3b8]">Battery</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-[#94a3b8]">Last Heartbeat</th>
            </tr>
          </thead>
          <tbody>
            {sensors.map((sensor) => (
              <SensorRow key={sensor.sensorId} sensor={sensor} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
