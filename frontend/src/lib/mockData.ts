/**
 * @fileoverview Mock data and utility functions for development and testing.
 * This module provides static data for assets, alerts, sensors, and other 
 * system components, along with functions to query and generate this data.
 */

import { Asset, Alert, SensorStatus, FFTBin, RULTrendPoint, FaultPrediction, Report, HealthTrend, SparePart, WorkOrder, CostAnalysis, ModelMetrics, AssetDocumentation, AuditEntry, ThermalAlert, TemperatureTrendPoint } from "./types";

export const mockAssets: Asset[] = [
  {
    id: "AST-001",
    name: "Compressor A1",
    type: "Centrifugal Compressor",
    location: "Plant Floor - Section A",
    status: "GREEN",
    rms: 1.8,
    rul: 2450,
    lastUpdated: new Date().toISOString(),
  },
  {
    id: "AST-002",
    name: "Pump Station B2",
    type: "Centrifugal Pump",
    location: "Plant Floor - Section B",
    status: "YELLOW",
    rms: 4.2,
    rul: 180,
    lastUpdated: new Date().toISOString(),
  },
  {
    id: "AST-003",
    name: "Motor Drive C3",
    type: "Induction Motor",
    location: "Plant Floor - Section C",
    status: "RED",
    rms: 7.1,
    rul: 24,
    lastUpdated: new Date().toISOString(),
  },
  {
    id: "AST-004",
    name: "Fan Unit D1",
    type: "Axial Fan",
    location: "Rooftop - HVAC",
    status: "GREEN",
    rms: 2.1,
    rul: 3200,
    lastUpdated: new Date().toISOString(),
  },
  {
    id: "AST-005",
    name: "Turbine E1",
    type: "Steam Turbine",
    location: "Power House",
    status: "YELLOW",
    rms: 5.8,
    rul: 72,
    lastUpdated: new Date().toISOString(),
  },
  {
    id: "AST-006",
    name: "Generator F1",
    type: "Sync Generator",
    location: "Power House",
    status: "GREEN",
    rms: 1.5,
    rul: 4800,
    lastUpdated: new Date().toISOString(),
  },
];

export const mockAlerts: Alert[] = [
  {
    id: "ALR-001",
    assetId: "AST-003",
    assetName: "Motor Drive C3",
    severity: "CRITICAL",
    message: "RMS exceeded critical threshold (7.1 mm/s)",
    timestamp: new Date(Date.now() - 300000).toISOString(),
  },
  {
    id: "ALR-002",
    assetId: "AST-002",
    assetName: "Pump Station B2",
    severity: "HIGH",
    message: "Degradation trend detected, RUL below 200 hours",
    timestamp: new Date(Date.now() - 1800000).toISOString(),
  },
  {
    id: "ALR-003",
    assetId: "AST-005",
    assetName: "Turbine E1",
    severity: "MEDIUM",
    message: "Abnormal vibration pattern detected",
    timestamp: new Date(Date.now() - 3600000).toISOString(),
  },
];

export const mockSensors: SensorStatus[] = [
  {
    sensorId: "SNS-001",
    name: "Vibration Sensor A1",
    status: "ONLINE",
    lastHeartbeat: new Date().toISOString(),
    batteryLevel: 85,
  },
  {
    sensorId: "SNS-002",
    name: "Temperature Sensor B2",
    status: "DEGRADED",
    lastHeartbeat: new Date(Date.now() - 600000).toISOString(),
    batteryLevel: 12,
  },
  {
    sensorId: "SNS-003",
    name: "Vibration Sensor C3",
    status: "OFFLINE",
    lastHeartbeat: new Date(Date.now() - 7200000).toISOString(),
    batteryLevel: 0,
  },
];

/**
 * Calculates high-level statistics for all mock assets.
 * 
 * @returns {Object} An object containing total, healthy, warning, and critical counts.
 */
export function getAssetStats() {
  const assets = mockAssets;
  return {
    total: assets.length,
    healthy: assets.filter((a) => a.status === "GREEN").length,
    warning: assets.filter((a) => a.status === "YELLOW").length,
    critical: assets.filter((a) => a.status === "RED").length,
  };
}

export const mockReports: Report[] = [
  {
    id: "RPT-001",
    name: "Weekly Asset Health Summary",
    type: "PDF",
    category: "HEALTH",
    assets: ["AST-001", "AST-002", "AST-003"],
    dateRange: { from: "2026-03-16", to: "2026-03-23" },
    createdAt: new Date(Date.now() - 86400000).toISOString(),
    status: "READY",
  },
  {
    id: "RPT-002",
    name: "Q1 ROI Analysis",
    type: "PDF",
    category: "ROI",
    assets: ["AST-001", "AST-002", "AST-003", "AST-004"],
    dateRange: { from: "2026-01-01", to: "2026-03-31" },
    createdAt: new Date(Date.now() - 172800000).toISOString(),
    status: "READY",
  },
  {
    id: "RPT-003",
    name: "Compliance Report March",
    type: "CSV",
    category: "COMPLIANCE",
    assets: ["AST-001", "AST-005", "AST-006"],
    dateRange: { from: "2026-03-01", to: "2026-03-23" },
    createdAt: new Date(Date.now() - 259200000).toISOString(),
    status: "READY",
  },
];

export const mockHealthTrend: HealthTrend[] = [
  { date: "Mar 17", healthy: 4, warning: 1, critical: 1 },
  { date: "Mar 18", healthy: 4, warning: 1, critical: 1 },
  { date: "Mar 19", healthy: 3, warning: 2, critical: 1 },
  { date: "Mar 20", healthy: 3, warning: 2, critical: 1 },
  { date: "Mar 21", healthy: 4, warning: 1, critical: 1 },
  { date: "Mar 22", healthy: 4, warning: 1, critical: 1 },
  { date: "Mar 23", healthy: 3, warning: 2, critical: 1 },
];

/**
 * Generates mock Fast Fourier Transform (FFT) vibration data for an asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {FFTBin[]} An array of FFT bins.
 */
function generateFFTData(assetId: string): FFTBin[] {
  const asset = mockAssets.find((a) => a.id === assetId);
  const bins: FFTBin[] = [];
  const baseMultiplier = asset ? (asset.rms / 2) : 1;
  
  for (let i = 0; i < 64; i++) {
    const frequency = i * 7.8125;
    let amplitude = Math.random() * 0.3;
    const baselineAmplitude = Math.random() * 0.2;
    
    if (frequency > 55 && frequency < 65) {
      amplitude += 1.2 * baseMultiplier;
    } else if (frequency > 115 && frequency < 125) {
      amplitude += 0.8 * baseMultiplier;
    } else if (frequency > 175 && frequency < 185) {
      amplitude += 0.5 * baseMultiplier;
    } else if (frequency > 235 && frequency < 245) {
      amplitude += 0.3 * baseMultiplier;
    }
    
    bins.push({ frequency: Math.round(frequency * 10) / 10, amplitude, baselineAmplitude });
  }
  return bins;
}

/**
 * Generates mock Remaining Useful Life (RUL) trend data for an asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {RULTrendPoint[]} An array of RUL trend points.
 */
function generateRULTrend(assetId: string): RULTrendPoint[] {
  const asset = mockAssets.find((a) => a.id === assetId);
  const currentRUL = asset?.rul || 100;
  const trend: RULTrendPoint[] = [];
  let rul = currentRUL + 144;
  
  for (let i = 6; i >= 0; i--) {
    const confidence = 95 - (6 - i) * 2 + Math.random() * 3;
    trend.push({
      date: `Mar ${17 + i}`,
      rul: Math.round(rul),
      confidence: Math.round(confidence),
    });
    rul -= 24;
  }
  return trend;
}

export const mockFaultPredictions: Record<string, FaultPrediction> = {
  "AST-001": { faultType: "Normal Operation", confidence: 92, description: "Machine operating within normal parameters" },
  "AST-002": { faultType: "Bearing Wear", confidence: 78, description: "Degradation detected in front bearing assembly" },
  "AST-003": { faultType: "Rotor Imbalance", confidence: 89, description: "Significant imbalance detected, immediate attention required" },
  "AST-004": { faultType: "Normal Operation", confidence: 94, description: "Machine operating within normal parameters" },
  "AST-005": { faultType: "Misalignment", confidence: 72, description: "Shaft misalignment suspected based on vibration pattern" },
  "AST-006": { faultType: "Normal Operation", confidence: 96, description: "Machine operating within normal parameters" },
};

export const mockFFTData: Record<string, FFTBin[]> = {};
export const mockRULTrendData: Record<string, RULTrendPoint[]> = {};

mockAssets.forEach((asset) => {
  mockFFTData[asset.id] = generateFFTData(asset.id);
  mockRULTrendData[asset.id] = generateRULTrend(asset.id);
});

/**
 * Retrieves an asset by its ID.
 * 
 * @param {string} id The ID of the asset.
 * @returns {Asset | undefined} The asset object if found, otherwise undefined.
 */
export function getAssetById(id: string): Asset | undefined {
  return mockAssets.find((a) => a.id === id);
}

/**
 * Retrieves mock FFT vibration data for a specific asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {FFTBin[]} An array of FFT bins.
 */
export function getFFTData(assetId: string): FFTBin[] {
  return mockFFTData[assetId] || [];
}

/**
 * Retrieves mock RUL trend data for a specific asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {RULTrendPoint[]} An array of RUL trend points.
 */
export function getRULTrend(assetId: string): RULTrendPoint[] {
  return mockRULTrendData[assetId] || [];
}

/**
 * Retrieves the fault prediction for a specific asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {FaultPrediction | undefined} The fault prediction object if found.
 */
export function getFaultPrediction(assetId: string): FaultPrediction | undefined {
  return mockFaultPredictions[assetId];
}

export const mockSpareParts: SparePart[] = [
  { id: "SP-001", name: "Bearing Assembly 6205", partNumber: "BRG-6205-2RS", category: "Bearings", stockLevel: 12, reorderPoint: 5, leadTimeDays: 14, unitCost: 45, supplier: "SKF Industries", status: "IN_STOCK" },
  { id: "SP-002", name: "Mechanical Seal 45mm", partNumber: "SEL-45MM-VIT", category: "Seals", stockLevel: 3, reorderPoint: 4, leadTimeDays: 21, unitCost: 280, supplier: "Flowserve Corp", status: "LOW_STOCK" },
  { id: "SP-003", name: "Coupling Element 32", partNumber: "CPL-32-NBR", category: "Couplings", stockLevel: 8, reorderPoint: 3, leadTimeDays: 10, unitCost: 120, supplier: "Renold Couplings", status: "IN_STOCK" },
  { id: "SP-004", name: "Drive Belt V-Profile", partNumber: "BLT-V65-SPZ", category: "Belts", stockLevel: 0, reorderPoint: 6, leadTimeDays: 7, unitCost: 35, supplier: "Gates Corporation", status: "OUT_OF_STOCK", assetId: "AST-003", rulThreshold: 72 },
  { id: "SP-005", name: "Motor Rotor Assembly", partNumber: "MTR-ROT-5HP", category: "Motors", stockLevel: 2, reorderPoint: 1, leadTimeDays: 45, unitCost: 2500, supplier: "Siemens AG", status: "IN_STOCK" },
  { id: "SP-006", name: "Vibration Damper 100mm", partNumber: "DMP-100-NR", category: "Mounts", stockLevel: 15, reorderPoint: 8, leadTimeDays: 12, unitCost: 65, supplier: "Ace Controls", status: "IN_STOCK" },
  { id: "SP-007", name: "Filter Element HF-40", partNumber: "FLT-HF40-10", category: "Filters", stockLevel: 4, reorderPoint: 10, leadTimeDays: 5, unitCost: 85, supplier: "Pall Corporation", status: "LOW_STOCK" },
  { id: "SP-008", name: "Lubricant ISO VG 68", partNumber: "LUB-68-20L", category: "Lubricants", stockLevel: 6, reorderPoint: 3, leadTimeDays: 3, unitCost: 120, supplier: "Shell Global", status: "IN_STOCK" },
  { id: "SP-009", name: "Sensor Module IQ8", partNumber: "SNS-IQ8-VIB", category: "Sensors", stockLevel: 1, reorderPoint: 2, leadTimeDays: 28, unitCost: 890, supplier: "Hansford Sensors", status: "LOW_STOCK", assetId: "AST-002", rulThreshold: 180 },
  { id: "SP-010", name: "Gasket Set Industrial", partNumber: "GSK-IND-STD", category: "Seals", stockLevel: 20, reorderPoint: 10, leadTimeDays: 7, unitCost: 25, supplier: "Gasket Engineering", status: "IN_STOCK" },
];

export const mockWorkOrders: WorkOrder[] = [
  { id: "WO-001", assetId: "AST-003", assetName: "Motor Drive C3", description: "Replace drive belt and inspect coupling alignment", priority: "CRITICAL", status: "IN_PROGRESS", requiredParts: [{ partId: "SP-004", quantity: 1 }], estimatedHours: 4, createdAt: new Date(Date.now() - 86400000).toISOString(), scheduledDate: "2026-03-24", assignedTo: "Raj Kumar" },
  { id: "WO-002", assetId: "AST-002", assetName: "Pump Station B2", description: "Replace bearing assembly and perform realignment", priority: "HIGH", status: "PENDING", requiredParts: [{ partId: "SP-001", quantity: 2 }, { partId: "SP-009", quantity: 1 }], estimatedHours: 6, createdAt: new Date(Date.now() - 172800000).toISOString(), scheduledDate: "2026-03-26" },
  { id: "WO-003", assetId: "AST-005", assetName: "Turbine E1", description: "Perform shaft alignment check and lubrication service", priority: "MEDIUM", status: "PENDING", requiredParts: [{ partId: "SP-008", quantity: 2 }], estimatedHours: 3, createdAt: new Date(Date.now() - 259200000).toISOString(), scheduledDate: "2026-03-28" },
  { id: "WO-004", assetId: "AST-001", assetName: "Compressor A1", description: "Quarterly maintenance - filter replacement", priority: "LOW", status: "COMPLETED", requiredParts: [{ partId: "SP-007", quantity: 2 }], estimatedHours: 2, createdAt: new Date(Date.now() - 604800000).toISOString(), completedAt: new Date(Date.now() - 432000000).toISOString(), assignedTo: "Raj Kumar" },
];

export const mockCostAnalysis: CostAnalysis[] = [
  { assetId: "AST-003", assetName: "Motor Drive C3", riskOfFailurePerHour: 5000, emergencyRepairCost: 15000, scheduledRepairCost: 6000, potentialDowntimeHours: 48, riskScore: 92, recommendation: "IMMEDIATE" },
  { assetId: "AST-002", assetName: "Pump Station B2", riskOfFailurePerHour: 2500, emergencyRepairCost: 12000, scheduledRepairCost: 5500, potentialDowntimeHours: 24, riskScore: 68, recommendation: "SCHEDULED" },
  { assetId: "AST-005", assetName: "Turbine E1", riskOfFailurePerHour: 3500, emergencyRepairCost: 20000, scheduledRepairCost: 8000, potentialDowntimeHours: 36, riskScore: 55, recommendation: "SCHEDULED" },
  { assetId: "AST-001", assetName: "Compressor A1", riskOfFailurePerHour: 1800, emergencyRepairCost: 8000, scheduledRepairCost: 3500, potentialDowntimeHours: 12, riskScore: 22, recommendation: "MONITOR" },
];

/**
 * Generates a collection of mock model performance metrics for the last 30 days.
 * 
 * @returns {ModelMetrics[]} An array of model metrics objects.
 */
function generateModelMetrics(): ModelMetrics[] {
  const metrics: ModelMetrics[] = [];
  for (let i = 30; i >= 0; i--) {
    const date = new Date(Date.now() - i * 86400000);
    const truePositives = Math.floor(15 + Math.random() * 10);
    const falsePositives = Math.floor(1 + Math.random() * 4);
    const trueNegatives = Math.floor(80 + Math.random() * 15);
    const falseNegatives = Math.floor(2 + Math.random() * 3);
    const total = truePositives + falsePositives + trueNegatives + falseNegatives;
    const precision = truePositives / (truePositives + falsePositives);
    const recall = truePositives / (truePositives + falseNegatives);
    const f1Score = 2 * (precision * recall) / (precision + recall);
    const fdr = falsePositives / (falsePositives + truePositives);
    metrics.push({
      date: date.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
      truePositives,
      falsePositives,
      trueNegatives,
      falseNegatives,
      precision: Math.round(precision * 1000) / 10,
      recall: Math.round(recall * 1000) / 10,
      f1Score: Math.round(f1Score * 1000) / 10,
      fdr: Math.round(fdr * 1000) / 10,
    });
  }
  return metrics;
}

export const mockModelMetrics = generateModelMetrics();

/**
 * Retrieves a spare part by its ID.
 * 
 * @param {string} id The ID of the spare part.
 * @returns {SparePart | undefined} The spare part object if found.
 */
export function getSparePartById(id: string): SparePart | undefined {
  return mockSpareParts.find((p) => p.id === id);
}

/**
 * Retrieves all work orders associated with a specific asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {WorkOrder[]} An array of work order objects.
 */
export function getWorkOrdersByAsset(assetId: string): WorkOrder[] {
  return mockWorkOrders.filter((wo) => wo.assetId === assetId);
}

/**
 * Identifies spare parts that require Just-in-Time (JIT) procurement based on RUL.
 * 
 * @returns {SparePart[]} An array of spare parts needing alerts.
 */
export function getJITAlerts(): SparePart[] {
  return mockSpareParts.filter((part) => {
    if (part.rulThreshold && part.assetId) {
      const asset = mockAssets.find((a) => a.id === part.assetId);
      if (asset) {
        const thresholdHours = part.leadTimeDays * 24 * 1.1;
        return asset.rul < thresholdHours;
      }
    }
    return false;
  });
}

export const mockAssetDocumentation: AssetDocumentation[] = [
  {
    assetId: "AST-001",
    assetName: "Compressor A1",
    schematics: [
      { name: "P&ID Diagram", url: "#", type: "PDF" },
      { name: "Assembly Drawing", url: "#", type: "DWG" },
      { name: "Electrical Schematic", url: "#", type: "PDF" },
    ],
    manuals: [
      { name: "Operation Manual", url: "#", pages: 45 },
      { name: "Maintenance Guide", url: "#", pages: 28 },
      { name: "Safety Instructions", url: "#", pages: 12 },
    ],
    mttrBenchmarks: [
      { task: "Filter Replacement", estimatedHours: 2 },
      { task: "Bearing Inspection", estimatedHours: 4 },
      { task: "Seal Replacement", estimatedHours: 3 },
      { task: "Full Overhaul", estimatedHours: 8 },
    ],
  },
  {
    assetId: "AST-002",
    assetName: "Pump Station B2",
    schematics: [
      { name: "Hydraulic Circuit", url: "#", type: "PDF" },
      { name: "Foundation Plan", url: "#", type: "DWG" },
    ],
    manuals: [
      { name: "Installation Guide", url: "#", pages: 35 },
      { name: "Troubleshooting Manual", url: "#", pages: 52 },
    ],
    mttrBenchmarks: [
      { task: "Bearing Replacement", estimatedHours: 6 },
      { task: "Seal Replacement", estimatedHours: 4 },
      { task: "Motor Rewind", estimatedHours: 24 },
      { task: "Impeller Replacement", estimatedHours: 8 },
    ],
  },
  {
    assetId: "AST-003",
    assetName: "Motor Drive C3",
    schematics: [
      { name: "Drive System Layout", url: "#", type: "PDF" },
      { name: "Belt Drive Assembly", url: "#", type: "DWG" },
      { name: "Control Panel Wiring", url: "#", type: "PDF" },
    ],
    manuals: [
      { name: "VFD Manual", url: "#", pages: 120 },
      { name: "Motor Specifications", url: "#", pages: 25 },
    ],
    mttrBenchmarks: [
      { task: "Belt Replacement", estimatedHours: 1 },
      { task: "Coupling Alignment", estimatedHours: 2 },
      { task: "Bearing Replacement", estimatedHours: 4 },
      { task: "Motor Replacement", estimatedHours: 6 },
    ],
  },
];

export const mockAuditTrail: AuditEntry[] = [
  {
    id: "AUD-001",
    assetId: "AST-003",
    assetName: "Motor Drive C3",
    technicianId: "TECH-001",
    technicianName: "Raj Kumar",
    action: "CHECK_IN",
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    location: { lat: 28.6139, lng: 77.2090 },
    qrValidated: true,
    workOrderId: "WO-001",
  },
  {
    id: "AUD-002",
    assetId: "AST-001",
    assetName: "Compressor A1",
    technicianId: "TECH-001",
    technicianName: "Raj Kumar",
    action: "CHECK_IN",
    timestamp: new Date(Date.now() - 86400000).toISOString(),
    location: { lat: 28.6139, lng: 77.2090 },
    qrValidated: true,
    workOrderId: "WO-004",
  },
  {
    id: "AUD-003",
    assetId: "AST-001",
    assetName: "Compressor A1",
    technicianId: "TECH-001",
    technicianName: "Raj Kumar",
    action: "CHECK_OUT",
    timestamp: new Date(Date.now() - 82800000).toISOString(),
    location: { lat: 28.6139, lng: 77.2090 },
    qrValidated: true,
    workOrderId: "WO-004",
  },
  {
    id: "AUD-004",
    assetId: "AST-002",
    assetName: "Pump Station B2",
    technicianId: "TECH-002",
    technicianName: "Amit Singh",
    action: "CHECK_IN",
    timestamp: new Date(Date.now() - 172800000).toISOString(),
    location: { lat: 28.6140, lng: 77.2095 },
    qrValidated: true,
  },
];

export const mockThermalAlerts: ThermalAlert[] = [
  {
    id: "TH-001",
    assetId: "AST-003",
    assetName: "Motor Drive C3",
    currentTemp: 92,
    baselineTemp: 65,
    durationMinutes: 12,
    severity: "CRITICAL",
    acknowledged: false,
    timestamp: new Date(Date.now() - 600000).toISOString(),
  },
  {
    id: "TH-002",
    assetId: "AST-005",
    assetName: "Turbine E1",
    currentTemp: 78,
    baselineTemp: 60,
    durationMinutes: 8,
    severity: "WARNING",
    acknowledged: false,
    timestamp: new Date(Date.now() - 1200000).toISOString(),
  },
  {
    id: "TH-003",
    assetId: "AST-002",
    assetName: "Pump Station B2",
    currentTemp: 85,
    baselineTemp: 62,
    durationMinutes: 25,
    severity: "CRITICAL",
    acknowledged: true,
    acknowledgedBy: "EHS Officer",
    acknowledgedAt: new Date(Date.now() - 300000).toISOString(),
    timestamp: new Date(Date.now() - 1800000).toISOString(),
  },
  {
    id: "TH-004",
    assetId: "AST-001",
    assetName: "Compressor A1",
    currentTemp: 72,
    baselineTemp: 58,
    durationMinutes: 15,
    severity: "WARNING",
    acknowledged: true,
    acknowledgedBy: "EHS Officer",
    acknowledgedAt: new Date(Date.now() - 3600000).toISOString(),
    timestamp: new Date(Date.now() - 7200000).toISOString(),
  },
];

/**
 * Generates mock temperature trend data for a specific asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @param {number} baselineTemp The baseline temperature for the asset.
 * @returns {TemperatureTrendPoint[]} An array of temperature trend points.
 */
function generateTemperatureTrend(assetId: string, baselineTemp: number): TemperatureTrendPoint[] {
  const points: TemperatureTrendPoint[] = [];
  for (let i = 24; i >= 0; i--) {
    const timestamp = new Date(Date.now() - i * 3600000);
    const variance = Math.sin(i / 4) * 5 + Math.random() * 3;
    const temp = baselineTemp + variance + (i < 4 ? 15 + (4 - i) * 3 : 0);
    points.push({
      timestamp: timestamp.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" }),
      temperature: Math.round(temp * 10) / 10,
    });
  }
  return points;
}

export const mockTemperatureTrends: Record<string, TemperatureTrendPoint[]> = {
  "AST-003": generateTemperatureTrend("AST-003", 65),
  "AST-005": generateTemperatureTrend("AST-005", 60),
  "AST-002": generateTemperatureTrend("AST-002", 62),
  "AST-001": generateTemperatureTrend("AST-001", 58),
};

/**
 * Retrieves maintenance documentation for a specific asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {AssetDocumentation | undefined} The asset documentation object if found.
 */
export function getDocumentationByAsset(assetId: string): AssetDocumentation | undefined {
  return mockAssetDocumentation.find((d) => d.assetId === assetId);
}

/**
 * Retrieves all thermal alerts associated with a specific asset.
 * 
 * @param {string} assetId The ID of the asset.
 * @returns {ThermalAlert[]} An array of thermal alert objects.
 */
export function getThermalAlertsByAsset(assetId: string): ThermalAlert[] {
  return mockThermalAlerts.filter((a) => a.assetId === assetId);
}

/**
 * Retrieves all thermal alerts that have not yet been acknowledged.
 * 
 * @returns {ThermalAlert[]} An array of unacknowledged thermal alerts.
 */
export function getUnacknowledgedThermalAlerts(): ThermalAlert[] {
  return mockThermalAlerts.filter((a) => !a.acknowledged);
}
