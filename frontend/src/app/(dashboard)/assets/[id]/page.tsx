"use client";

import { useState, useEffect, use } from "react";
import { notFound } from "next/navigation";
import { api } from "@/lib/api";
import { Asset, SensorDataPoint, RULTrendPoint, FaultPrediction } from "@/lib/types";
import { AssetDetailHeader } from "@/components/dashboard/AssetDetailHeader";
import { FFTChart } from "@/components/dashboard/FFTChart";
import { RULTrendChart } from "@/components/dashboard/RULTrendChart";
import { FaultBadge } from "@/components/dashboard/FaultBadge";

interface AssetDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function AssetDetailPage({ params }: AssetDetailPageProps) {
  const { id } = use(params);
  const [asset, setAsset] = useState<Asset | null>(null);
  const [telemetry, setTelemetry] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [assetsData, telData, predData] = await Promise.all([
          api.getAssets(),
          api.getAssetTelemetry(id),
          api.getAssetPredictions(id)
        ]);

        const currentAsset = assetsData.find((a: Asset) => a.id === id);
        if (!currentAsset) {
          setError("Asset not found");
          return;
        }

        setAsset(currentAsset);
        setTelemetry(telData);
        setPredictions(predData);
      } catch (err: any) {
        console.error("Failed to load asset data", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadData();
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-[#94a3b8]">Loading asset details...</div>
      </div>
    );
  }

  if (error || !asset) {
    return (
      <div className="p-6 text-center">
        <h1 className="text-xl font-bold text-[#f1f5f9] mb-2">Error</h1>
        <p className="text-[#94a3b8]">{error || "Asset not found"}</p>
      </div>
    );
  }

  // Transform data for charts
  const fftData: SensorDataPoint[] = telemetry.map((t, idx) => ({
    frequency: idx, // Simplified since we don't have real FFT yet
    amplitude: t.vibration || 0
  })).slice(-50); // Last 50 points

  const rulTrend: RULTrendPoint[] = predictions.map(p => ({
    date: new Date(p._time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    rul: p.predicted_rul_hours || 0,
    confidence: p.confidence_score_percent || 0
  })).slice(-20); // Last 20 predictions

  const latestPred = predictions[predictions.length - 1];
  const faultPrediction: FaultPrediction | null = latestPred ? {
    type: latestPred.predicted_fault_type || "Normal",
    confidence: latestPred.confidence_score_percent || 0,
    timestamp: latestPred._time,
    recommendation: latestPred.risk_level === "High-Risk" ? "Immediate Maintenance Required" : "Schedule Maintenance"
  } : null;

  return (
    <div className="p-6 space-y-6">
      <AssetDetailHeader asset={asset} />

      {faultPrediction && (
        <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
          <h2 className="text-sm font-medium text-[#f1f5f9] mb-3">Fault Prediction</h2>
          <FaultBadge prediction={faultPrediction} />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
          <h2 className="text-sm font-medium text-[#f1f5f9] mb-4">Vibration Trend (Live)</h2>
          <FFTChart data={fftData} />
        </div>

        <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
          <h2 className="text-sm font-medium text-[#f1f5f9] mb-4">RUL Trend (Live)</h2>
          <RULTrendChart data={rulTrend} />
        </div>
      </div>
    </div>
  );
}
