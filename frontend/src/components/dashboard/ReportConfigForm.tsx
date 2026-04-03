/**
 * @file ReportConfigForm component for configuring report generation settings.
 */

"use client";

import { useState } from "react";
import { ReportCategory, ReportType } from "@/lib/types";
import { ReportTypeSelector } from "./ReportTypeSelector";

interface ReportConfigFormProps {
  onGenerate: (config: {
    type: ReportType;
    category: ReportCategory;
    assets: string[];
    dateRange: { from: string; to: string };
  }) => void;
}

const categories: { value: ReportCategory; label: string }[] = [
  { value: "HEALTH", label: "Asset Health" },
  { value: "ROI", label: "ROI Analysis" },
  { value: "COMPLIANCE", label: "Compliance" },
];

const assetOptions = [
  { id: "AST-001", name: "Compressor A1" },
  { id: "AST-002", name: "Pump Station B2" },
  { id: "AST-003", name: "Motor Drive C3" },
  { id: "AST-004", name: "Fan Unit D1" },
  { id: "AST-005", name: "Turbine E1" },
  { id: "AST-006", name: "Generator F1" },
];

/**
 * A form for configuring and triggering report generation.
 * 
 * @param {ReportConfigFormProps} props The component props.
 * @param {function(object): void} props.onGenerate Callback triggered when the generate button is clicked.
 * @returns {JSX.Element} The rendered report configuration form.
 */
export function ReportConfigForm({ onGenerate }: ReportConfigFormProps) {
  const [type, setType] = useState<ReportType>("PDF");
  const [category, setCategory] = useState<ReportCategory>("HEALTH");
  const [selectedAssets, setSelectedAssets] = useState<string[]>([]);
  const [dateFrom, setDateFrom] = useState("2026-03-01");
  const [dateTo, setDateTo] = useState("2026-03-23");

  /**
   * Handles the report generation trigger.
   */
  const handleGenerate = () => {
    onGenerate({ type, category, assets: selectedAssets, dateRange: { from: dateFrom, to: dateTo } });
  };

  /**
   * Toggles asset selection.
   * 
   * @param {string} id The asset ID to toggle.
   */
  const toggleAsset = (id: string) => {
    setSelectedAssets((prev) =>
      prev.includes(id) ? prev.filter((a) => a !== id) : [...prev, id]
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-[#f1f5f9] mb-2">Report Type</label>
        <ReportTypeSelector value={type} onChange={setType} />
      </div>

      <div>
        <label className="block text-sm font-medium text-[#f1f5f9] mb-2">Category</label>
        <div className="flex gap-2">
          {categories.map((cat) => (
            <button
              key={cat.value}
              type="button"
              onClick={() => setCategory(cat.value)}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                category === cat.value
                  ? "bg-[#3b82f6] text-white"
                  : "bg-[#1e293b] text-[#94a3b8] hover:text-[#f1f5f9] hover:bg-[#334155]"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-[#f1f5f9] mb-2">Assets</label>
        <div className="flex flex-wrap gap-2">
          {assetOptions.map((asset) => (
            <button
              key={asset.id}
              type="button"
              onClick={() => toggleAsset(asset.id)}
              className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
                selectedAssets.includes(asset.id)
                  ? "bg-[#3b82f6] text-white"
                  : "bg-[#1e293b] text-[#94a3b8] hover:text-[#f1f5f9] hover:bg-[#334155] border border-[#334155]"
              }`}
            >
              {asset.name}
            </button>
          ))}
        </div>
        {selectedAssets.length === 0 && (
          <p className="mt-1 text-xs text-[#64748b]">All assets will be included if none selected</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-[#f1f5f9] mb-2">From</label>
          <input
            type="date"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            className="w-full px-3 py-2 bg-[#1e293b] border border-[#334155] rounded-lg text-sm text-[#f1f5f9] focus:outline-none focus:border-[#3b82f6]"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#f1f5f9] mb-2">To</label>
          <input
            type="date"
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            className="w-full px-3 py-2 bg-[#1e293b] border border-[#334155] rounded-lg text-sm text-[#f1f5f9] focus:outline-none focus:border-[#3b82f6]"
          />
        </div>
      </div>

      <button
        type="button"
        onClick={handleGenerate}
        className="w-full py-2.5 bg-[#3b82f6] hover:bg-[#2563eb] text-white font-medium rounded-lg transition-colors"
      >
        Generate Report
      </button>
    </div>
  );
}
