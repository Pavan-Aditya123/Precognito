/**
 * @fileoverview Layout wrapper for all dashboard-related pages.
 * Handles user authentication checks, sidebar navigation, header display, 
 * and offline status indicators.
 */

"use client";

import { Sidebar } from "@/components/dashboard/Sidebar";
import { Header } from "@/components/dashboard/Header";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { OfflineIndicator } from "@/components/ui/OfflineIndicator";

/**
 * DashboardLayout component that provides common UI structure for dashboard pages.
 * 
 * @param {Object} props Component properties.
 * @param {React.ReactNode} props.children The page content to be rendered within the layout.
 * @returns {JSX.Element|null} The rendered dashboard layout or null during redirection.
 */
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  useEffect(() => {
    /**
     * Redirects to login if the session is not valid.
     */
    if (!isPending && !session) {
      router.push("/login");
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0f172a]">
        <div className="text-[#94a3b8]">Loading session...</div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <div className="flex-1 ml-[248px] flex flex-col">
        <Header />
        <main className="flex-1 p-6">{children}</main>
      </div>
      <OfflineIndicator />
    </div>
  );
}
