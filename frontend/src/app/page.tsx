/**
 * @file Root page of the application, which redirects to the marketing landing page.
 */

import LandingPage from "@/app/(marketing)/page";

/**
 * Renders the home page.
 * 
 * @returns {JSX.Element} The rendered landing page.
 */
export default function Home() {
  return <LandingPage />;
}
