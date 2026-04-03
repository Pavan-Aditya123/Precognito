/**
 * @fileoverview Better Auth server-side configuration.
 */

import { betterAuth } from "better-auth";
import { Database } from "bun:sqlite";

/**
 * Better Auth server configuration with SQLite database.
 */
export const auth = betterAuth({
  database: new Database("precognito.sqlite"),
  emailAndPassword: {
    enabled: true,
  },
  user: {
    additionalFields: {
      role: {
        type: "string",
        required: false,
        defaultValue: "TECHNICIAN",
      }
    }
  }
});
