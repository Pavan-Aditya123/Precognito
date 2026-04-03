/**
 * @fileoverview Executive dashboard page for high-level decision support.
 * This module provides key performance indicators (KPIs) such as Overall Equipment 
 * Effectiveness (OEE), risk assessments, and cost-benefit analysis for management.
 */

"use client";

import { useState, useEffect } from "react";
import { mockCostAnalysis } from "@/lib/mockData";
import { RiskGauge } from "@/components/dashboard/RiskGauge";
import { CostComparisonCard } from "@/components/dashboard/CostComparisonCard";
import { DowntimeKPIs } from "@/components/dashboard/DowntimeKPIs";
import { api } from "@/lib/api";

/**
 * ExecutivePage component for high-level plant performance oversight.
 * 
 * @returns {JSX.Element} The rendered executive dashboard.
 */
export default function ExecutivePage() {
  const [oeeData, setOeeData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const costAnalysis = mockCostAnalysis;

  useEffect(() => {
    /**
     * Fetches OEE metrics from the API.
     */
    async function loadOEE() {
      try {
        const data = await api.getOEEMetrics();
        setOeeData(data);
      } catch (err) {
        console.error("Failed to load OEE metrics", err);
      } finally {
        setLoading(false);
      }
    }
    loadOEE();
  }, []);

  const sortedByRisk = [...costAnalysis].sort((a, b) => b.riskScore - a.riskScore);
  const criticalAssets = costAnalysis.filter((ca) => ca.recommendation === "IMMEDIATE");

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-[#94a3b8]">Loading executive insights...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-[#f1f5f9]">Executive Decision Support</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-[#94a3b8]">
            OEE Score: <span className="text-[#22c55e] font-bold">{oeeData?.oee}%</span>
          </span>
          {criticalAssets.length > 0 && (
            <span className="px-2 py-1 rounded bg-[#ef4444]/20 text-[#ef4444] text-xs">
              {criticalAssets.length} Critical Assets
            </span>
          )}
        </div>
      </div>

      {/* OEE Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-6 border border-[#334155] rounded-lg bg-[#1e293b]">
          <p className="text-sm text-[#94a3b8] mb-1">Availability</p>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold text-[#f1f5f9]">{oeeData?.availability}%</p>
            <span className="text-xs text-[#22c55e] mb-1">↑ 0.5%</span>
          </div>
          <div className="mt-4 h-1.5 bg-[#334155] rounded-full overflow-hidden">
            <div className="h-full bg-[#3b82f6] rounded-full" style={{ width: `${oeeData?.availability}%` }} />
          </div>
        </div>
        <div className="p-6 border border-[#334155] rounded-lg bg-[#1e293b]">
          <p className="text-sm text-[#94a3b8] mb-1">Performance</p>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold text-[#f1f5f9]">{oeeData?.performance}%</p>
            <span className="text-xs text-[#ef4444] mb-1">↓ 1.2%</span>
          </div>
          <div className="mt-4 h-1.5 bg-[#334155] rounded-full overflow-hidden">
            <div className="h-full bg-[#8b5cf6] rounded-full" style={{ width: `${oeeData?.performance}%` }} />
          </div>
        </div>
        <div className="p-6 border border-[#334155] rounded-lg bg-[#1e293b]">
          <p className="text-sm text-[#94a3b8] mb-1">Quality</p>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold text-[#f1f5f9]">{oeeData?.quality}%</p>
            <span className="text-xs text-[#22c55e] mb-1">↑ 0.1%</span>
          </div>
          <div className="mt-4 h-1.5 bg-[#334155] rounded-full overflow-hidden">
            <div className="h-full bg-[#22c55e] rounded-full" style={{ width: `${oeeData?.quality}%` }} />
          </div>
        </div>
      </div>

      <DowntimeKPIs costAnalysisList={costAnalysis} />

      <section>
        <h2 className="text-lg font-medium text-[#f1f5f9] mb-3">Risk Assessment by Asset</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {sortedByRisk.map((ca) => (
            <RiskGauge key={ca.assetId} costAnalysis={ca} />
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-lg font-medium text-[#f1f5f9] mb-3">Cost-Benefit Analysis</h2>
        <p className="text-sm text-[#94a3b8] mb-4">
          Compare emergency repair costs vs scheduled maintenance to optimize maintenance budget
        </p>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {sortedByRisk.map((ca) => (
            <CostComparisonCard key={ca.assetId} costAnalysis={ca} />
          ))}
        </div>
      </section>

      {criticalAssets.length > 0 && (
        <section className="border border-[#ef4444] rounded-lg p-4 bg-[#ef4444]/5">
          <h2 className="text-lg font-medium text-[#ef4444] mb-2">Urgent Recommendations</h2>
          <ul className="space-y-2">
            {criticalAssets.map((ca) => (
              <li key={ca.assetId} className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-[#ef4444]" />
                <span className="text-[#f1f5f9]">
                  <strong>{ca.assetName}</strong>: Risk of failure at ${ca.riskOfFailurePerHour.toLocaleString()}/hr.
                  Schedule repair now to save ${(ca.emergencyRepairCost - ca.scheduledRepairCost).toLocaleString()}.
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
