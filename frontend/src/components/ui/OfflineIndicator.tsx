/**
 * @file OfflineIndicator component that alerts the user when they are offline.
 */

"use client";

import { useState, useEffect } from "react";

/**
 * A fixed-position indicator that appears when the application is offline.
 * 
 * @returns {JSX.Element | null} The offline indicator or null if online.
 */
export function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    // Set initial state
    setIsOnline(navigator.onLine);

    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (isOnline) return null;

  return (
    <div className="fixed bottom-4 right-4 z-[100] animate-in fade-in slide-in-from-bottom-2">
      <div className="flex items-center gap-2 px-4 py-2 bg-[#ef4444] text-white text-sm font-medium rounded-lg shadow-lg border border-[#ef4444]/50">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-3.536 5 5 0 011.414-3.536m-1.202 1.202L3.929 3.929m14.435 14.435L3.93 3.93" />
        </svg>
        <span>Offline Mode - Data is from cache</span>
      </div>
    </div>
  );
}
