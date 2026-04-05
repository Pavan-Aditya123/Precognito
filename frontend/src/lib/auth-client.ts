/**
 * @fileoverview Auth client for Better Auth.
 */

import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client instance for client-side authentication.
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

/** Sign in method from authClient. */
export const { signIn, signOut, useSession } = authClient;
