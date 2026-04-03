export type AssetStatus = "GREEN" | "YELLOW" | "RED";

export interface Asset {
  id: string;
  name: string;
  type: string;
  location: string;
  status: AssetStatus;
  rms: number;
  rul: number;
  lastUpdated: string;
}

export interface Alert {
  id: string;
  assetId: string;
  assetName: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  message: string;
  timestamp: string;
}

export interface SensorStatus {
  sensorId: string;
  name: string;
  status: "ONLINE" | "OFFLINE" | "DEGRADED";
  lastHeartbeat: string;
  batteryLevel: number;
}

export type ReportType = "PDF" | "CSV";
export type ReportCategory = "HEALTH" | "ROI" | "COMPLIANCE";
export type ReportStatus = "READY" | "GENERATING";

export interface Report {
  id: string;
  name: string;
  type: ReportType;
  category: ReportCategory;
  assets: string[];
  dateRange: { from: string; to: string };
  createdAt: string;
  status: ReportStatus;
}

export interface HealthTrend {
  date: string;
  healthy: number;
  warning: number;
  critical: number;
}

export interface FFTBin {
  frequency: number;
  amplitude: number;
  baselineAmplitude: number;
}

export interface RULTrendPoint {
  date: string;
  rul: number;
  confidence: number;
}

export interface FaultPrediction {
  faultType: string;
  confidence: number;
  description: string;
}

export type PartStatus = "IN_STOCK" | "LOW_STOCK" | "OUT_OF_STOCK" | "ORDERED";

export interface SparePart {
  id: string;
  name: string;
  partNumber: string;
  category: string;
  stockLevel: number;
  reorderPoint: number;
  leadTimeDays: number;
  unitCost: number;
  supplier: string;
  status: PartStatus;
  assetId?: string;
  rulThreshold?: number;
}

export type WorkOrderPriority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type WorkOrderStatus = "PENDING" | "IN_PROGRESS" | "COMPLETED" | "CANCELLED";

export interface WorkOrder {
  id: string;
  assetId: string;
  assetName: string;
  description: string;
  priority: WorkOrderPriority;
  status: WorkOrderStatus;
  requiredParts: { partId: string; quantity: number }[];
  estimatedHours: number;
  createdAt: string;
  scheduledDate?: string;
  completedAt?: string;
  assignedTo?: string;
}

export interface CostAnalysis {
  assetId: string;
  assetName: string;
  riskOfFailurePerHour: number;
  emergencyRepairCost: number;
  scheduledRepairCost: number;
  potentialDowntimeHours: number;
  riskScore: number;
  recommendation: "IMMEDIATE" | "SCHEDULED" | "MONITOR";
}

export interface ModelMetrics {
  date: string;
  truePositives: number;
  falsePositives: number;
  trueNegatives: number;
  falseNegatives: number;
  precision: number;
  recall: number;
  f1Score: number;
  fdr: number;
}

export interface MTTRBenchmark {
  task: string;
  estimatedHours: number;
}

export interface AssetDocumentation {
  assetId: string;
  assetName: string;
  schematics: { name: string; url: string; type: string }[];
  manuals: { name: string; url: string; pages: number }[];
  mttrBenchmarks: MTTRBenchmark[];
}

export interface GeoLocation {
  lat: number;
  lng: number;
}

export interface AuditEntry {
  id: string;
  assetId: string;
  assetName: string;
  technicianId: string;
  technicianName: string;
  action: "CHECK_IN" | "CHECK_OUT";
  timestamp: string;
  location: GeoLocation;
  qrValidated: boolean;
  workOrderId?: string;
}

export type ThermalSeverity = "WARNING" | "CRITICAL";

export interface ThermalAlert {
  id: string;
  assetId: string;
  assetName: string;
  currentTemp: number;
  baselineTemp: number;
  durationMinutes: number;
  severity: ThermalSeverity;
  acknowledged: boolean;
  acknowledgedBy?: string;
  acknowledgedAt?: string;
  timestamp: string;
}

export interface TemperatureTrendPoint {
  timestamp: string;
  temperature: number;
}
