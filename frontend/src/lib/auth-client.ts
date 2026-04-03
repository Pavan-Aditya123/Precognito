/**
 * @fileoverview Auth client for Better Auth.
 */

import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client instance.
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

export const { signIn, signOut, useSession } = authClient;
