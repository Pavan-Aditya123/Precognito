/**
 * @fileoverview Layout wrapper for authentication-related pages.
 * Provides a common container for login, registration, and password recovery pages.
 */

/**
 * AuthLayout component that wraps authentication pages.
 * 
 * @param {Object} props Component properties.
 * @param {React.ReactNode} props.children The authentication page content.
 * @returns {JSX.Element} The rendered authentication layout.
 */
export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
