/**
 * @fileoverview Authentication route handler for the Better Auth library.
 * This module exports the GET and POST handlers for all auth-related API requests.
 */

import { auth } from "@/lib/auth";

export const GET = auth.handler;
export const POST = auth.handler;
