export type UserRole = "ADMIN" | "MANAGER" | "OT_SPECIALIST" | "TECHNICIAN" | "STORE_MANAGER";

export const roleColors: Record<UserRole, string> = {
  ADMIN: "#ef4444",
  MANAGER: "#8b5cf6",
  OT_SPECIALIST: "#3b82f6",
  TECHNICIAN: "#22c55e",
  STORE_MANAGER: "#eab308",
};

export const rolePermissions: Record<UserRole, string[]> = {
  ADMIN: ["assets", "alerts", "edge", "reports", "inventory", "work-orders", "executive", "analytics", "ehs", "admin"],
  MANAGER: ["assets", "reports", "executive", "analytics"],
  OT_SPECIALIST: ["assets", "alerts", "edge", "ehs"],
  TECHNICIAN: ["assets", "alerts", "work-orders"],
  STORE_MANAGER: ["inventory"],
};
