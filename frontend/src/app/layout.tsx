/**
 * @fileoverview Root layout component for the entire Next.js application.
 * This module defines the HTML structure, global styles, metadata, 
 * and viewport configurations for all pages.
 */

import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Precognito - Predictive Maintenance",
  description: "IoT-enabled Predictive Maintenance System for industrial assets",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "Precognito",
  },
  formatDetection: {
    telephone: false,
  },
};

export const viewport: Viewport = {
  themeColor: "#0f172a",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: "cover",
};

/**
 * RootLayout component that serves as the top-level wrapper for all pages.
 * 
 * @param {Object} props Component properties.
 * @param {React.ReactNode} props.children The content to be rendered within the layout.
 * @returns {JSX.Element} The rendered root layout.
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <head>
        <meta name="application-name" content="Precognito" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Precognito" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="msapplication-TileColor" content="#0f172a" />
        <meta name="msapplication-tap-highlight" content="no" />
      </head>
      <body className="h-full antialiased">
        {children}
      </body>
    </html>
  );
}
