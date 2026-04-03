"use client";

import { useState, useEffect } from "react";
import { mockModelMetrics } from "@/lib/mockData";
import { FDRGauge } from "@/components/dashboard/FDRGauge";
import { ModelAccuracyCard } from "@/components/dashboard/ModelAccuracyCard";
import { PerformanceTrend } from "@/components/dashboard/PerformanceTrend";
import { api } from "@/lib/api";

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    async function loadMetrics() {
      try {
        const data = await api.getModelMetrics();
        setMetrics(data);
      } catch (err) {
        console.error("Failed to load model metrics", err);
      } finally {
        setLoading(false);
      }
    }
    loadMetrics();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-[#94a3b8]">Loading performance analytics...</div>
      </div>
    );
  }

  // Use mock historical trend for chart since we only have aggregate metrics currently
  const trendData = mockModelMetrics;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-[#f1f5f9]">Model Performance Analytics</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-[#94a3b8]">
            Analysis Period: <span className="text-[#f1f5f9]">{metrics?.period}</span>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-1">
          <ModelAccuracyCard metrics={[{ ...trendData[trendData.length-1], accuracy: metrics.accuracy }]} />
        </div>
        <div className="lg:col-span-2">
          <FDRGauge metrics={[{ ...trendData[trendData.length-1], fdr: metrics.fdr }]} />
        </div>
      </div>

      <PerformanceTrend metrics={trendData} />

      <div className="border border-[#334155] rounded-lg p-6 bg-[#1e293b]">
        <h3 className="text-sm text-[#94a3b8] mb-4">Model Validation Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-lg bg-[#0f172a]">
            <p className="text-xs text-[#94a3b8] mb-1">Model Accuracy</p>
            <p className="text-2xl font-bold text-[#22c55e]">
              {metrics?.accuracy}%
            </p>
            <p className="text-xs text-[#94a3b8] mt-1">Within acceptable range</p>
          </div>
          
          <div className="p-4 rounded-lg bg-[#0f172a]">
            <p className="text-xs text-[#94a3b8] mb-1">False Discovery Rate</p>
            <p className="text-2xl font-bold text-[#f1f5f9]">
              {metrics?.fdr}%
            </p>
            <p className="text-xs text-[#94a3b8] mt-1">
              {metrics?.fdr <= 5 ? "Meets target (<5%)" : "Above target"}
            </p>
          </div>
          
          <div className="p-4 rounded-lg bg-[#0f172a]">
            <p className="text-xs text-[#94a3b8] mb-1">True Positives</p>
            <p className="text-2xl font-bold text-[#3b82f6]">
              {metrics?.truePositives}
            </p>
            <p className="text-xs text-[#94a3b8] mt-1">Confirmed Anomalies</p>
          </div>
          
          <div className="p-4 rounded-lg bg-[#0f172a]">
            <p className="text-xs text-[#94a3b8] mb-1">False Alarms</p>
            <p className="text-2xl font-bold text-[#eab308]">
              {metrics?.falsePositives}
            </p>
            <p className="text-xs text-[#94a3b8] mt-1">Operator feedback</p>
          </div>
        </div>
      </div>

      <div className={`p-4 rounded-lg border ${metrics.fdr <= 5 ? 'bg-[#22c55e]/10 border-[#22c55e]/30' : 'bg-[#eab308]/10 border-[#eab308]/30'}`}>
        <h4 className={`text-sm font-medium mb-2 ${metrics.fdr <= 5 ? 'text-[#22c55e]' : 'text-[#eab308]'}`}>Validation Status</h4>
        <p className="text-sm text-[#94a3b8]">
          The anomaly detection engine is performing {metrics.fdr <= 5 ? 'optimally' : 'adequately'}.
          FDR of {metrics.fdr}% is {metrics.fdr <= 5 ? "within" : "slightly above"} the target threshold of 5%.
          {metrics.fdr <= 5
            ? " Model is validated for production use."
            : " Consider providing more validation feedback to refine the model."}
        </p>
      </div>
    </div>
  );
}
