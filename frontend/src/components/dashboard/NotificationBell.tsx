/**
 * @file NotificationBell component for real-time alerts using Server-Sent Events (SSE).
 */

"use client";

import { useState, useEffect } from "react";
import { ThermalAlert } from "@/lib/types";

interface NotificationBellProps {
  alerts?: ThermalAlert[]; // Existing alerts from DB
}

/**
 * Renders a notification bell that listens to real-time alerts via SSE (ntfy.sh).
 * 
 * @param {NotificationBellProps} props The component props.
 * @param {ThermalAlert[]} [props.alerts=[]] Initial set of alerts.
 * @returns {JSX.Element} The rendered notification bell and dropdown.
 */
export function NotificationBell({ alerts = [] }: NotificationBellProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [realTimeAlerts, setRealTimeAlerts] = useState<any[]>([]);

  useEffect(() => {
    // NTFY Topic URL for SSE
    const topic = "precognito_alerts_demo";
    const eventSource = new EventSource(`https://ntfy.sh/${topic}/sse`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("New Real-time Alert:", data);
        
        // ntfy sse returns various message types, we only care about 'message'
        if (data.event === "message") {
          const newAlert = {
            id: data.id,
            title: data.title || "Alert",
            message: data.message,
            time: new Date(data.time * 1000).toLocaleTimeString(),
            priority: data.priority,
            tags: data.tags || []
          };
          
          setRealTimeAlerts((prev) => [newAlert, ...prev].slice(0, 10));
          
          // Play a subtle notification sound if browser allows
          const audio = new Audio("https://ntfy.sh/static/media/notification.mp3");
          audio.play().catch(() => {}); 
        }
      } catch (err) {
        console.error("Failed to parse real-time alert", err);
      }
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const unacknowledgedCount = realTimeAlerts.length;

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-[#94a3b8] hover:text-[#f1f5f9] transition-colors"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>
        {unacknowledgedCount > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center bg-[#ef4444] text-white text-[10px] font-bold rounded-full animate-bounce">
            {unacknowledgedCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 top-full mt-2 w-80 bg-[#1e293b] border border-[#334155] rounded-lg shadow-xl z-50 overflow-hidden">
            <div className="p-3 border-b border-[#334155] flex items-center justify-between">
              <h3 className="text-sm font-medium text-[#f1f5f9]">
                Live Notifications
              </h3>
              <button
                className="text-xs text-[#3b82f6] hover:underline"
                onClick={() => setRealTimeAlerts([])}
              >
                Clear All
              </button>
            </div>
            <div className="max-h-80 overflow-y-auto">
              {realTimeAlerts.length > 0 ? (
                realTimeAlerts.map((alert) => (
                  <div
                    key={alert.id}
                    className="block p-3 border-b border-[#334155] last:border-0 hover:bg-[#0f172a] transition-colors"
                  >
                    <div className="flex items-start gap-2">
                      <span
                        className={`w-2 h-2 mt-1.5 rounded-full ${
                          alert.priority >= 4
                            ? "bg-[#ef4444]"
                            : "bg-[#eab308]"
                        }`}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-bold text-[#f1f5f9]">
                          {alert.title}
                        </p>
                        <p className="text-xs text-[#94a3b8] mt-0.5 leading-relaxed">
                          {alert.message}
                        </p>
                        <p className="text-[10px] text-[#64748b] mt-1">
                          {alert.time}
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-8 text-center text-[#94a3b8] text-sm">
                  <p>No new notifications</p>
                  <p className="text-[10px] mt-2 opacity-50 font-mono">Listening to: precognito_alerts_demo</p>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
