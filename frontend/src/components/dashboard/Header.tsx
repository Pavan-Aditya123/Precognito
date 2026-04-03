/**
 * @file Header component for the application's top navigation bar.
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import { api } from "@/lib/api";
import { NotificationBell } from "./NotificationBell";
import { roleColors } from "@/lib/constants";

/**
 * Renders the top navigation header with logo, notifications, and user profile dropdown.
 * 
 * @returns {JSX.Element | null} The rendered header or null if user is not logged in.
 */
export function Header() {
  const { data: session } = useSession();
  const user = session?.user;
  const router = useRouter();
  const [showDropdown, setShowDropdown] = useState(false);

  /**
   * Handles user sign out and redirection to the login page.
   */
  const handleLogout = async () => {
    await signOut();
    router.push("/login");
  };

  if (!user) return null;

  // @ts-ignore
  const role = user.role || "TECHNICIAN";

  return (
    <header
      className="h-14 px-4 flex items-center justify-between border-b border-[#334155]"
      style={{ backgroundColor: "#0f172a" }}
    >
      <div className="flex items-center gap-4">
        <Link href="/dashboard" className="font-semibold text-[#f1f5f9]">
          Precognito
        </Link>
      </div>

      <div className="flex items-center gap-4">
        <NotificationBell />

        <div className="relative">
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="flex items-center gap-2 p-2 rounded-lg hover:bg-[#1e293b] transition-colors"
          >
            <div className="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium" style={{ backgroundColor: roleColors[role as any] || "#3b82f6" }}>
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div className="text-left hidden sm:block">
              <p className="text-sm text-[#f1f5f9]">{user.name}</p>
              <p className="text-xs text-[#94a3b8]">{role.replace(/_/g, " ")}</p>
            </div>
            <svg className="w-4 h-4 text-[#94a3b8]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {showDropdown && (
            <>
              <div className="fixed inset-0 z-40" onClick={() => setShowDropdown(false)} />
              <div className="absolute right-0 top-full mt-2 w-48 bg-[#1e293b] border border-[#334155] rounded-lg shadow-xl z-50 overflow-hidden">
                <div className="p-3 border-b border-[#334155]">
                  <p className="text-sm text-[#f1f5f9]">{user.name}</p>
                  <p className="text-xs text-[#94a3b8]">{user.email}</p>
                </div>
                <Link
                  href="/dashboard"
                  className="block px-3 py-2 text-sm text-[#f1f5f9] hover:bg-[#334155] transition-colors"
                  onClick={() => setShowDropdown(false)}
                >
                  Dashboard
                </Link>
                <button
                  onClick={() => {
                    handleLogout();
                    setShowDropdown(false);
                  }}
                  className="w-full text-left px-3 py-2 text-sm text-[#ef4444] hover:bg-[#334155] transition-colors"
                >
                  Logout
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
