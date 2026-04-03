/**
 * @file ReportList component for displaying a history of generated reports.
 */

"use client";

import { Report } from "@/lib/types";

interface ReportListProps {
  reports: Report[];
  onDownload?: (report: Report) => void;
}

/**
 * Formats an ISO date string into a readable format (e.g., "Mar 23, 2026").
 * 
 * @param {string} isoString The ISO date string.
 * @returns {string} The formatted date string.
 */
function formatDate(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

/**
 * Gets a human-readable label for a report category.
 * 
 * @param {string} category The category key.
 * @returns {string} The display label for the category.
 */
function getCategoryLabel(category: string): string {
  const labels: Record<string, string> = {
    HEALTH: "Health",
    ROI: "ROI",
    COMPLIANCE: "Compliance",
  };
  return labels[category] || category;
}

/**
 * Renders a list of generated reports with download actions.
 * 
 * @param {ReportListProps} props The component props.
 * @param {Report[]} props.reports Array of generated reports.
 * @param {function(Report): void} [props.onDownload] Callback when a download button is clicked.
 * @returns {JSX.Element} The rendered report list.
 */
export function ReportList({ reports, onDownload }: ReportListProps) {
  if (reports.length === 0) {
    return (
      <div className="text-center py-12 text-[#94a3b8]">
        No reports generated yet
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {reports.map((report) => (
        <div
          key={report.id}
          className="flex items-center justify-between p-4 bg-[#1e293b] border border-[#334155] rounded-lg hover:border-[#3b82f6] transition-colors"
        >
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 flex items-center justify-center bg-[#334155] rounded-lg">
              <span className="text-xs font-medium text-[#94a3b8]">{report.type}</span>
            </div>
            <div>
              <h3 className="text-sm font-medium text-[#f1f5f9]">{report.name}</h3>
              <p className="text-xs text-[#94a3b8] mt-0.5">
                {getCategoryLabel(report.category)} · {report.assets.length} assets · {formatDate(report.createdAt)}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="px-2 py-1 text-xs font-medium bg-[#22c55e]/20 text-[#22c55e] rounded">
              {report.status}
            </span>
            <button 
              onClick={() => onDownload?.(report)}
              className="p-2 text-[#94a3b8] hover:text-[#f1f5f9] transition-colors"
              title="Download Report"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
