/**
 * @fileoverview Type definitions for the application's data models and UI state.
 */

/** Possible asset health statuses. */
export type AssetStatus = "GREEN" | "YELLOW" | "RED";

/** Represents a machine or component in the facility. */
export interface Asset {
  /** Unique identifier for the asset. */
  id: string;
  /** Human-readable name of the asset. */
  name: string;
  /** Category of the asset (e.g., Pump, Motor). */
  type: string;
  /** Physical location of the asset. */
  location: string;
  /** Current health status. */
  status: AssetStatus;
  /** Root Mean Square (vibration intensity). */
  rms: number;
  /** Remaining Useful Life in days. */
  rul: number;
  /** ISO timestamp of the last data update. */
  lastUpdated: string;
}

/** Represents an anomaly or critical event detected for an asset. */
export interface Alert {
  /** Unique identifier for the alert. */
  id: string;
  /** ID of the associated asset. */
  assetId: string;
  /** Name of the associated asset. */
  assetName: string;
  /** Importance level of the alert. */
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  /** Descriptive message about the alert. */
  message: string;
  /** ISO timestamp when the alert was triggered. */
  timestamp: string;
}

/** Represents the connectivity and health of a hardware sensor. */
export interface SensorStatus {
  /** Unique hardware identifier. */
  sensorId: string;
  /** Human-readable name. */
  name: string;
  /** Current connectivity state. */
  status: "ONLINE" | "OFFLINE" | "DEGRADED";
  /** ISO timestamp of the last received heartbeat. */
  lastHeartbeat: string;
  /** Battery percentage (0-100). */
  batteryLevel: number;
}

/** Supported report formats. */
export type ReportType = "PDF" | "CSV";
/** Categories for report grouping. */
export type ReportCategory = "HEALTH" | "ROI" | "COMPLIANCE";
/** Generation status of a report. */
export type ReportStatus = "READY" | "GENERATING";

/** Represents a generated or queued report. */
export interface Report {
  /** Unique identifier. */
  id: string;
  /** Name of the report. */
  name: string;
  /** Export format. */
  type: ReportType;
  /** Report category. */
  category: ReportCategory;
  /** IDs of assets included in this report. */
  assets: string[];
  /** Start and end dates for the report data. */
  dateRange: { from: string; to: string };
  /** ISO timestamp when the report was requested. */
  createdAt: string;
  /** Current generation status. */
  status: ReportStatus;
}

/** Represents a data point for asset health trends over time. */
export interface HealthTrend {
  /** Date of the snapshot. */
  date: string;
  /** Count of healthy assets. */
  healthy: number;
  /** Count of assets with warnings. */
  warning: number;
  /** Count of critical assets. */
  critical: number;
}

/** Represents a frequency bin in a vibration FFT analysis. */
export interface FFTBin {
  /** Frequency in Hz. */
  frequency: number;
  /** Current amplitude value. */
  amplitude: number;
  /** Historical baseline amplitude for comparison. */
  baselineAmplitude: number;
}

/** Represents a historical RUL prediction data point. */
export interface RULTrendPoint {
  /** Date of the prediction. */
  date: string;
  /** Predicted Remaining Useful Life in days. */
  rul: number;
  /** Confidence level of the prediction (0-1). */
  confidence: number;
}

/** Represents a specific fault type prediction. */
export interface FaultPrediction {
  /** Type of fault detected (e.g., Bearing Failure). */
  faultType: string;
  /** Probability of this fault type (0-1). */
  confidence: number;
  /** Detailed description of the fault and symptoms. */
  description: string;
}

/** Possible availability statuses for spare parts. */
export type PartStatus = "IN_STOCK" | "LOW_STOCK" | "OUT_OF_STOCK" | "ORDERED";

/** Represents a spare part in the inventory. */
export interface SparePart {
  /** Unique identifier. */
  id: string;
  /** Human-readable name. */
  name: string;
  /** SKU or manufacturer part number. */
  partNumber: string;
  /** Category (e.g., Bearings, Lubricants). */
  category: string;
  /** Current quantity in the warehouse. */
  stockLevel: number;
  /** Threshold below which an order should be placed. */
  reorderPoint: number;
  /** Typical time to receive after ordering. */
  leadTimeDays: number;
  /** Price per unit. */
  unitCost: number;
  /** Name of the vendor. */
  supplier: string;
  /** Inventory status. */
  status: PartStatus;
  /** Optional ID of an asset this part is specifically for. */
  assetId?: string;
  /** Optional RUL threshold to trigger JIT ordering. */
  rulThreshold?: number;
}

/** Priority levels for maintenance work orders. */
export type WorkOrderPriority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
/** Lifecycle statuses for work orders. */
export type WorkOrderStatus = "PENDING" | "IN_PROGRESS" | "COMPLETED" | "CANCELLED";

/** Represents a maintenance task. */
export interface WorkOrder {
  /** Unique identifier. */
  id: string;
  /** ID of the asset requiring maintenance. */
  assetId: string;
  /** Name of the asset. */
  assetName: string;
  /** Description of the work to be performed. */
  description: string;
  /** Task priority. */
  priority: WorkOrderPriority;
  /** Current progress status. */
  status: WorkOrderStatus;
  /** Parts required for the task. */
  requiredParts: { partId: string; quantity: number }[];
  /** Estimated duration in hours. */
  estimatedHours: number;
  /** ISO timestamp when the order was created. */
  createdAt: string;
  /** Scheduled date for the work. */
  scheduledDate?: string;
  /** ISO timestamp when the work was finished. */
  completedAt?: string;
  /** Name or ID of the assigned technician. */
  assignedTo?: string;
}

/** Represents a financial risk analysis for an asset. */
export interface CostAnalysis {
  /** Asset ID. */
  assetId: string;
  /** Asset Name. */
  assetName: string;
  /** Estimated cost of failure per hour. */
  riskOfFailurePerHour: number;
  /** Cost if the asset fails unexpectedly. */
  emergencyRepairCost: number;
  /** Cost if the repair is planned. */
  scheduledRepairCost: number;
  /** Hours of downtime expected if failed. */
  potentialDowntimeHours: number;
  /** Calculated risk score. */
  riskScore: number;
  /** Recommended action. */
  recommendation: "IMMEDIATE" | "SCHEDULED" | "MONITOR";
}

/** Represents ML model performance metrics. */
export interface ModelMetrics {
  /** Date of the metrics snapshot. */
  date: string;
  /** Count of true positives. */
  truePositives: number;
  /** Count of false positives. */
  falsePositives: number;
  /** Count of true negatives. */
  trueNegatives: number;
  /** Count of false negatives. */
  falseNegatives: number;
  /** Precision score (0-1). */
  precision: number;
  /** Recall score (0-1). */
  recall: number;
  /** F1 score (0-1). */
  f1Score: number;
  /** False Discovery Rate (0-1). */
  fdr: number;
}

/** Benchmark for Mean Time To Repair. */
export interface MTTRBenchmark {
  /** Description of the maintenance task. */
  task: string;
  /** Standard estimated duration in hours. */
  estimatedHours: number;
}

/** Collection of documentation for an asset. */
export interface AssetDocumentation {
  /** Asset ID. */
  assetId: string;
  /** Asset Name. */
  assetName: string;
  /** List of technical schematics. */
  schematics: { name: string; url: string; type: string }[];
  /** List of operation/maintenance manuals. */
  manuals: { name: string; url: string; pages: number }[];
  /** Industry benchmarks for repairs. */
  mttrBenchmarks: MTTRBenchmark[];
}

/** Geographic coordinates. */
export interface GeoLocation {
  /** Latitude. */
  lat: number;
  /** Longitude. */
  lng: number;
}

/** Entry in the maintenance audit trail. */
export interface AuditEntry {
  /** Unique identifier. */
  id: string;
  /** Asset ID. */
  assetId: string;
  /** Asset Name. */
  assetName: string;
  /** Technician ID. */
  technicianId?: string;
  /** Technician Name. */
  technicianName: string;
  /** Description of the action taken. */
  action: string;
  /** ISO timestamp of the action. */
  timestamp: string;
  /** Location where the action was recorded. */
  location: GeoLocation;
  /** Whether the asset QR code was scanned. */
  qrValidated: boolean;
  /** Optional linked work order ID. */
  workOrderId?: string;
  /** Recorded Mean Time To Repair for this action. */
  mttr?: string;
}

/** Severity levels for thermal alerts. */
export type ThermalSeverity = "WARNING" | "CRITICAL";

/** Represents a thermal anomaly alert. */
export interface ThermalAlert {
  /** Unique identifier. */
  id: string;
  /** Asset ID. */
  assetId: string;
  /** Asset Name. */
  assetName: string;
  /** Measured temperature in Celsius. */
  currentTemp: number;
  /** Baseline temperature for comparison. */
  baselineTemp: number;
  /** How long the anomaly has persisted. */
  durationMinutes: number;
  /** Alert severity. */
  severity: ThermalSeverity;
  /** Whether the alert has been acknowledged. */
  acknowledged: boolean;
  /** Who acknowledged the alert. */
  acknowledgedBy?: string;
  /** ISO timestamp of acknowledgement. */
  acknowledgedAt?: string;
  /** ISO timestamp when the alert was triggered. */
  timestamp: string;
}

/** Represents a point in a temperature trend over time. */
export interface TemperatureTrendPoint {
  /** ISO timestamp. */
  timestamp: string;
  /** Temperature in Celsius. */
  temperature: number;
}
