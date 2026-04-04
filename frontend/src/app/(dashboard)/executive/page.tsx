"use client";

import { useState, useEffect } from "react";
import { RiskGauge } from "@/components/dashboard/RiskGauge";
import { CostComparisonCard } from "@/components/dashboard/CostComparisonCard";
import { DowntimeKPIs } from "@/components/dashboard/DowntimeKPIs";
import { api } from "@/lib/api";

/**
 * @fileoverview Executive Dashboard Page for ROI and Financial Analytics.
 * @returns {JSX.Element} The rendered executive page.
 */
export default function ExecutivePage() {
  const [oeeData, setOeeData] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadExecutiveData() {
      try {
        const [oee, recs] = await Promise.all([
          api.getOEEMetrics(),
          api.getRecommendations()
        ]);
        setOeeData(oee);
        setRecommendations(recs.recommendations || []);
      } catch (err) {
        console.error("Failed to load executive data", err);
      } finally {
        setLoading(false);
      }
    }
    loadExecutiveData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-[#94a3b8]">Loading executive insights...</div>
      </div>
    );
  }

  // Calculate high-risk assets from real recommendations
  const highRiskAssets = recommendations.filter(r => r.failure_probability > 0.7 || r.rul < 0.15);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-[#f1f5f9]">Executive Decision Support</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-[#94a3b8]">
            OEE Score: <span className="text-[#22c55e] font-bold">{oeeData?.oee}%</span>
          </span>
          {highRiskAssets.length > 0 && (
            <span className="px-2 py-1 rounded bg-[#ef4444]/20 text-[#ef4444] text-xs">
              {highRiskAssets.length} High Risk Components
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
            <span className="text-xs text-[#22c55e] mb-1">Live</span>
          </div>
          <div className="mt-4 h-1.5 bg-[#334155] rounded-full overflow-hidden">
            <div className="h-full bg-[#3b82f6] rounded-full" style={{ width: `${oeeData?.availability}%` }} />
          </div>
        </div>
        <div className="p-6 border border-[#334155] rounded-lg bg-[#1e293b]">
          <p className="text-sm text-[#94a3b8] mb-1">Performance</p>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold text-[#f1f5f9]">{oeeData?.performance}%</p>
            <span className="text-xs text-[#8b5cf6] mb-1">Live</span>
          </div>
          <div className="mt-4 h-1.5 bg-[#334155] rounded-full overflow-hidden">
            <div className="h-full bg-[#8b5cf6] rounded-full" style={{ width: `${oeeData?.performance}%` }} />
          </div>
        </div>
        <div className="p-6 border border-[#334155] rounded-lg bg-[#1e293b]">
          <p className="text-sm text-[#94a3b8] mb-1">Quality</p>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold text-[#f1f5f9]">{oeeData?.quality}%</p>
            <span className="text-xs text-[#22c55e] mb-1">Live</span>
          </div>
          <div className="mt-4 h-1.5 bg-[#334155] rounded-full overflow-hidden">
            <div className="h-full bg-[#22c55e] rounded-full" style={{ width: `${oeeData?.quality}%` }} />
          </div>
        </div>
      </div>

      {/* Financial KPIs */}
      <div className="p-6 border border-[#334155] rounded-lg bg-[#1e293b]">
        <h2 className="text-lg font-medium text-[#f1f5f9] mb-4">Financial Impact (30 Day Rolling)</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <p className="text-sm text-[#94a3b8] mb-1">Total Downtime Avoided</p>
            <p className="text-4xl font-bold text-[#22c55e]">{oeeData?.downtimeAvoidedHours} hours</p>
            <p className="text-xs text-[#64748b] mt-2">Based on early detection of critical anomalies</p>
          </div>
          <div>
            <p className="text-sm text-[#94a3b8] mb-1">Estimated Cost Savings</p>
            <p className="text-4xl font-bold text-[#3b82f6]">${oeeData?.costSavings?.toLocaleString()}</p>
            <p className="text-xs text-[#64748b] mt-2">Calculated from avoided emergency repair labor & parts</p>
          </div>
        </div>
      </div>

      <section>
        <h2 className="text-lg font-medium text-[#f1f5f9] mb-3">AI Recommendations & Cost Analysis</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {recommendations.slice(0, 6).map((rec, idx) => (
            <div key={idx} className="p-4 border border-[#334155] rounded-lg bg-[#1e293b] space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium text-[#f1f5f9]">{rec.component}</h3>
                  <p className="text-xs text-[#94a3b8] font-mono">{rec.machine_id}</p>
                </div>
                <span className={`px-2 py-1 rounded text-[10px] font-bold ${
                  rec.decision === 'Replace' ? 'bg-[#ef4444]/20 text-[#ef4444]' : 'bg-[#3b82f6]/20 text-[#3b82f6]'
                }`}>
                  {rec.decision.toUpperCase()}
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-[#94a3b8] text-xs">Estimated Cost</p>
                  <p className="font-semibold text-[#f1f5f9]">${rec.final_cost.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-[#94a3b8] text-xs">Failure Prob.</p>
                  <p className={`font-semibold ${rec.failure_probability > 0.5 ? 'text-[#ef4444]' : 'text-[#22c55e]'}`}>
                    {(rec.failure_probability * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              <div className="p-2 rounded bg-[#0f172a] border border-[#334155]">
                <p className="text-[11px] text-[#3b82f6] font-medium uppercase tracking-wider mb-1">Recommendation</p>
                <p className="text-xs text-[#f1f5f9]">{rec.recommendation}</p>
                <p className="text-[10px] text-[#64748b] mt-1">{rec.explanation}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {highRiskAssets.length > 0 && (
        <section className="border border-[#ef4444] rounded-lg p-4 bg-[#ef4444]/5">
          <h2 className="text-lg font-medium text-[#ef4444] mb-2">Urgent Financial Risk</h2>
          <ul className="space-y-2">
            {highRiskAssets.map((rec, idx) => (
              <li key={idx} className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-[#ef4444]" />
                <span className="text-[#f1f5f9]">
                  <strong>{rec.machine_id} - {rec.component}</strong>: High failure probability. Action required to avoid unplanned downtime costs.
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
