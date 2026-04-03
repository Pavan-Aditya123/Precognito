"use client";

import { Asset } from "@/lib/types";
import { StatusBadge } from "@/components/ui/StatusBadge";

interface AssetDetailHeaderProps {
  asset: Asset;
}

function formatRUL(hours: number): string {
  if (hours < 24) return `${hours} hrs`;
  const days = Math.floor(hours / 24);
  const remainingHours = hours % 24;
  if (remainingHours === 0) return `${days} days`;
  return `${days}d ${remainingHours}h`;
}

export function AssetDetailHeader({ asset }: AssetDetailHeaderProps) {
  const statusColor = {
    GREEN: "bg-[#22c55e]",
    YELLOW: "bg-[#eab308]",
    RED: "bg-[#ef4444]",
  }[asset.status];

  const rulIsLow = asset.rul < 168;

  return (
    <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h1 className="text-xl font-semibold text-[#f1f5f9]">{asset.name}</h1>
            <StatusBadge status={asset.status} />
          </div>
          <p className="text-sm text-[#94a3b8]">{asset.type}</p>
          <p className="text-sm text-[#64748b]">{asset.location}</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6 mt-6">
        <div className="bg-[#0f172a] rounded-lg p-4">
          <p className="text-xs text-[#94a3b8] mb-1">RMS Velocity</p>
          <p className="text-2xl font-semibold text-[#f1f5f9]">{asset.rms.toFixed(1)} <span className="text-sm text-[#64748b]">mm/s</span></p>
          <div className="mt-2 h-2 bg-[#334155] rounded-full overflow-hidden">
            <div 
              className={`h-full rounded-full ${statusColor}`}
              style={{ width: `${Math.min((asset.rms / 8) * 100, 100)}%` }}
            />
          </div>
        </div>

        <div className="bg-[#0f172a] rounded-lg p-4">
          <p className="text-xs text-[#94a3b8] mb-1">Remaining Useful Life</p>
          <p className={`text-2xl font-semibold ${rulIsLow ? "text-[#ef4444]" : "text-[#f1f5f9]"}`}>
            {formatRUL(asset.rul)}
          </p>
          <p className="text-xs text-[#64748b] mt-1">
            {asset.rul >= 720 
              ? "> 30 days" 
              : asset.rul >= 168 
                ? "1-30 days" 
                : "< 7 days"}
          </p>
        </div>

        <div className="bg-[#0f172a] rounded-lg p-4">
          <p className="text-xs text-[#94a3b8] mb-1">Last Updated</p>
          <p className="text-lg font-medium text-[#f1f5f9]">
            {asset.lastUpdated ? new Date(asset.lastUpdated).toLocaleTimeString("en-US", { 
              hour: "2-digit", 
              minute: "2-digit" 
            }) : "Never"}
          </p>
          <p className="text-xs text-[#64748b] mt-1">
            {asset.lastUpdated ? new Date(asset.lastUpdated).toLocaleDateString("en-US", { 
              month: "short", 
              day: "numeric" 
            }) : "-"}
          </p>
        </div>
      </div>
    </div>
  );
}