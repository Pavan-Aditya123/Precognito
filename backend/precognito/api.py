"""
Main FastAPI application entry point for the Precognito backend.
Coordinates database connections, authentication, auditing, and routing.
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from typing import Optional
import asyncpg
import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Import routers from other modules
from precognito.work_orders.api import router as workorder_router
from precognito.inventory.api import router as inventory_router

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://precognito_user:precognito_password@localhost:5432/precognito")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for handling application startup and shutdown events.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Startup: Initialize DB Pool
    app.db_pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    # Shutdown: Close DB Pool
    if hasattr(app, "db_pool"):
        await app.db_pool.close()

app = FastAPI(lifespan=lifespan)

async def get_db_pool():
    """Dependency that returns the global database connection pool.

    Returns:
        asyncpg.Pool: The database connection pool.
    """
    return app.db_pool

async def get_current_user(request: Request, pool = Depends(get_db_pool)):
    """Authenticates the user based on session tokens or Bearer tokens.

    Args:
        request (Request): The incoming FastAPI request.
        pool (asyncpg.Pool): Database connection pool dependency.

    Raises:
        HTTPException: If authentication fails or session is invalid/expired.

    Returns:
        asyncpg.Record: The authenticated user record.
    """
    session_token = request.cookies.get("better-auth.session_token")
    if not session_token:
        # Check Authorization header too
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split(" ")[1]
            
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async with pool.acquire() as conn:
        # Better Auth stores sessions in 'session' table
        session = await conn.fetchrow(
            'SELECT "userId", "expiresAt" FROM "session" WHERE "token" = $1',
            session_token
        )
        
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
            
        # Check expiry (asyncpg returns datetime)
        if session["expiresAt"].replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Session expired")
            
        user = await conn.fetchrow(
            'SELECT * FROM "user" WHERE "id" = $1',
            session["userId"]
        )
        return user

class RoleChecker:
    """Dependency for performing Role-Based Access Control (RBAC).

    Attributes:
        allowed_roles (list[str]): List of roles permitted to access the resource.
    """
    def __init__(self, allowed_roles: list[str]):
        """Initializes the RoleChecker with allowed roles.

        Args:
            allowed_roles (list[str]): Roles that have access.
        """
        self.allowed_roles = allowed_roles

    def __call__(self, user = Depends(get_current_user)):
        """Check if the authenticated user has one of the allowed roles.

        Args:
            user (asyncpg.Record): The authenticated user.

        Raises:
            HTTPException: If the user's role is not authorized.

        Returns:
            asyncpg.Record: The authorized user record.
        """
        if user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail=f"Role '{user['role']}' does not have permission to access this resource"
            )
        return user

# Role dependencies
admin_only = Depends(RoleChecker(["ADMIN"]))
manager_above = Depends(RoleChecker(["ADMIN", "MANAGER"]))
lead_above = Depends(RoleChecker(["ADMIN", "MANAGER", "OT_SPECIALIST"]))
store_manager_above = Depends(RoleChecker(["ADMIN", "STORE_MANAGER"]))

# Include Routers
# Module 4: Work Orders
app.include_router(workorder_router)
# Module 3: Inventory & Supply Chain
app.include_router(inventory_router)

async def log_audit_action(pool, user_id: str, action: str, resource: str, details: str = None):
    """Logs a user action to the audit log table.

    Args:
        pool (asyncpg.Pool): Database connection pool.
        user_id (str): ID of the user performing the action.
        action (str): The action performed (e.g., 'SUBMIT_FEEDBACK').
        resource (str): The resource affected (e.g., 'anomaly:123').
        details (str, optional): Additional JSON or text details. Defaults to None.
    """
    async with pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO "audit_log" ("userId", "action", "resource", "details") VALUES ($1, $2, $3, $4)',
            user_id, action, resource, details
        )

@app.get("/audit-logs")
async def get_audit_logs(user = admin_only, pool = Depends(get_db_pool)):
    """API endpoint to retrieve recent audit logs. Restricted to admins.

    Args:
        user: Authenticated admin user dependency.
        pool: Database connection pool dependency.

    Returns:
        list: A list of recent audit log entries with user names.
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            'SELECT a.*, u.name as "userName" FROM "audit_log" a JOIN "user" u ON a."userId" = u.id ORDER BY a.timestamp DESC LIMIT 100'
        )
        return [dict(r) for r in rows]

@app.post("/model-feedback")
async def submit_model_feedback(data: dict, user = Depends(get_current_user), pool = Depends(get_db_pool)):
    """Submits user feedback regarding the accuracy of an anomaly detection.

    Args:
        data (dict): Feedback data (anomalyId, deviceId, isReal).
        user: Authenticated user dependency.
        pool: Database connection pool dependency.

    Raises:
        HTTPException: If required fields are missing.

    Returns:
        dict: Success status.
    """
    anomaly_id = data.get("anomalyId")
    device_id = data.get("deviceId")
    is_real = data.get("isReal")

    if not all([anomaly_id, device_id]) or is_real is None:
        raise HTTPException(status_code=400, detail="Missing required fields")

    async with pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO "model_feedback" ("anomalyId", "deviceId", "isReal", "userId") VALUES ($1, $2, $3, $4)',
            anomaly_id, device_id, is_real, user["id"]
        )
        await log_audit_action(pool, user["id"], "SUBMIT_FEEDBACK", f"anomaly:{anomaly_id}", f"is_real:{is_real}")

    return {"status": "success"}

@app.get("/analytics/metrics")
async def get_model_metrics(user = lead_above, pool = Depends(get_db_pool)):
    """Calculates ML model performance metrics based on user feedback.

    Args:
        user: Authorized lead user dependency.
        pool: Database connection pool dependency.

    Returns:
        dict: Accuracy, FDR, and confusion matrix counts.
    """
    async with pool.acquire() as conn:
        # Calculate metrics from feedback
        total_feedback = await conn.fetchval('SELECT COUNT(*) FROM "model_feedback"')
        true_positives = await conn.fetchval('SELECT COUNT(*) FROM "model_feedback" WHERE "isReal" = true')
        false_positives = await conn.fetchval('SELECT COUNT(*) FROM "model_feedback" WHERE "isReal" = false')

        # Mock some negatives since we don't have user feedback for non-anomalies usually
        true_negatives = 1000 # Mocked for prototype
        false_negatives = 2 # Mocked for prototype

        total = true_positives + false_positives + true_negatives + false_negatives
        accuracy = (true_positives + true_negatives) / total if total > 0 else 0.95
        fdr = false_positives / (true_positives + false_positives) * 100 if (true_positives + false_positives) > 0 else 2.5

        return {
            "accuracy": round(accuracy * 100, 1),
            "fdr": round(fdr, 1),
            "truePositives": true_positives,
            "falsePositives": false_positives,
            "trueNegatives": true_negatives,
            "falseNegatives": false_negatives,
            "period": "30 days"
        }

@app.get("/analytics/oee")
async def get_oee_metrics(device_id: Optional[str] = None, user = manager_above):
    """Retrieves Overall Equipment Effectiveness (OEE) metrics.

    Args:
        device_id (str, optional): Filter by specific device.
        user: Authorized manager dependency.

    Returns:
        dict: OEE components and calculated values.
    """
    # Simple OEE calculation for prototype
    # In production, this would query historical data over shifts
    return {
        "availability": 98.5,
        "performance": 94.2,
        "quality": 99.1,
        "oee": 91.8,
        "downtimeAvoidedHours": 124,
        "costSavings": 45000
    }

@app.get("/")
def home():
    """Health check endpoint.

    Returns:
        dict: Welcome message.
    """
    return {"message": "Precognito Backend Running"}

@app.post("/ingest")
async def ingest_data(data: dict, user = Depends(get_current_user)):
    """API endpoint for authenticated telemetry ingestion.

    Args:
        data (dict): Telemetry data.
        user: Authenticated user dependency.

    Raises:
        HTTPException: If device_id is missing or ingestion fails.

    Returns:
        dict: Ingestion result and user information.
    """
    from precognito.ingestion.core import process_ingestion

    device_id = data.get("device_id")
    if not device_id:
        raise HTTPException(status_code=400, detail="device_id is required")

    result = process_ingestion(device_id, data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Ingestion processing failed")

    return {
        **result,
        "status": "success",
        "user": user["name"]
    }

@app.get("/assets")
async def get_assets(user = Depends(get_current_user)):
    """Retrieves all assets with their latest telemetry and predictive status.

    Args:
        user: Authenticated user dependency.

    Returns:
        list: A list of asset objects including health status and RUL.
    """
    from precognito.ingestion.influx_client import get_all_devices, query_latest_data
    
    device_ids = get_all_devices()
    assets = []
    
    for d_id in device_ids:
        # Get latest telemetry
        tel_tables = query_latest_data(d_id, "machine_telemetry")
        # Get latest prediction
        pred_tables = query_latest_data(d_id, "predictive_results")
        
        asset_info = {
            "id": d_id,
            "name": " ".join([s.capitalize() for s in d_id.split("_")]),
            "status": "GREEN", # Default
            "rms": 0.0,
            "rul": 0.0,
            "lastUpdated": None
        }
        
        if tel_tables:
            for table in tel_tables:
                for record in table.records:
                    if record.get_field() == "vibration_rms":
                        asset_info["rms"] = record.get_value()
                    asset_info["lastUpdated"] = record.get_time().isoformat()
        
        if pred_tables:
            for table in pred_tables:
                for record in table.records:
                    if record.get_field() == "predicted_rul_hours":
                        asset_info["rul"] = record.get_value()
                    if record.get_field() == "risk_level":
                        risk = record.get_value()
                        if risk == "High-Risk": asset_info["status"] = "RED"
                        elif risk == "Warning": asset_info["status"] = "YELLOW"
        
        assets.append(asset_info)
        
    return assets

@app.get("/assets/{device_id}/telemetry")
async def get_asset_telemetry(device_id: str, range: str = "-24h", user = Depends(get_current_user)):
    """Retrieves historical telemetry for a specific asset.

    Args:
        device_id (str): The ID of the asset.
        range (str, optional): Time range for history. Defaults to "-24h".
        user: Authenticated user dependency.

    Returns:
        list: Historical telemetry records.
    """
    from precognito.ingestion.influx_client import query_historical_data
    
    tables = query_historical_data(device_id, "machine_telemetry", range)
    results = []
    
    for table in tables:
        for record in table.records:
            results.append(record.values)
            
    return results

@app.get("/assets/{device_id}/predictions")
async def get_asset_predictions(device_id: str, range: str = "-24h", user = Depends(get_current_user)):
    """Retrieves historical predictive results for a specific asset.

    Args:
        device_id (str): The ID of the asset.
        range (str, optional): Time range for history. Defaults to "-24h".
        user: Authenticated user dependency.

    Returns:
        list: Historical predictive results.
    """
    from precognito.ingestion.influx_client import query_historical_data
    
    tables = query_historical_data(device_id, "predictive_results", range)
    results = []
    
    for table in tables:
        for record in table.records:
            results.append(record.values)
            
    return results

@app.get("/alerts")
async def get_all_alerts(range: str = "-24h", user = Depends(get_current_user)):
    """Retrieves all anomaly alerts within a specific time range.

    Args:
        range (str, optional): Time range for alerts. Defaults to "-24h".
        user: Authenticated user dependency.

    Returns:
        list: A list of detected anomalies.
    """
    from precognito.ingestion.influx_client import INFLUX_BUCKET, INFLUX_ORG, query_api
    
    query = f'from(bucket: "{INFLUX_BUCKET}") |> range(start: {range}) |> filter(fn: (r) => r["_measurement"] == "anomaly_results") |> filter(fn: (r) => r["_field"] == "anomaly_detected") |> filter(fn: (r) => r["_value"] == true) |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
    
    tables = query_api.query(query, org=INFLUX_ORG)
    results = []
    
    for table in tables:
        for record in table.records:
            results.append({
                "id": f"{record.get_time().timestamp()}-{record.values.get('device_id')}",
                "deviceId": record.values.get("device_id"),
                "severity": record.values.get("severity"),
                "message": record.values.get("reason"),
                "timestamp": record.get_time().isoformat(),
                "acknowledged": False
            })
            
    # Sort by timestamp descending
    results.sort(key=lambda x: x["timestamp"], reverse=True)
    return results

@app.get("/safety-alerts")
async def get_safety_alerts(range: str = "-24h", user = lead_above):
    """Retrieves all safety alerts (e.g., thermal breaches) within a time range.

    Args:
        range (str, optional): Time range for alerts. Defaults to "-24h".
        user: Authorized lead user dependency.

    Returns:
        list: A list of safety alerts.
    """
    from precognito.ingestion.influx_client import INFLUX_BUCKET, INFLUX_ORG, query_api
    
    query = f'from(bucket: "{INFLUX_BUCKET}") |> range(start: {range}) |> filter(fn: (r) => r["_measurement"] == "safety_alerts") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
    
    tables = query_api.query(query, org=INFLUX_ORG)
    results = []
    
    for table in tables:
        for record in table.records:
            results.append({
                "id": f"safety-{record.get_time().timestamp()}",
                "assetId": record.values.get("device_id"),
                "assetName": " ".join([s.capitalize() for s in record.values.get("device_id").split("_")]),
                "severity": "CRITICAL",
                "type": record.values.get("type"),
                "currentTemp": record.values.get("temperature"),
                "baselineTemp": 60.0,
                "timestamp": record.get_time().isoformat(),
                "acknowledged": False
            })
            
    return results

@app.post("/ingest/dev")
async def ingest_data_dev(data: dict):
    """Unauthenticated ingestion endpoint for development and testing.

    Args:
        data (dict): Telemetry data.

    Raises:
        HTTPException: If device_id is missing or ingestion fails.

    Returns:
        dict: Ingestion result.
    """
    from precognito.ingestion.core import process_ingestion

    device_id = data.get("device_id")
    if not device_id:
        raise HTTPException(status_code=400, detail="device_id is required")

    result = process_ingestion(device_id, data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Ingestion processing failed")

    return {
        **result,
        "status": "success",
        "user": "dev_user"
    }

@app.get("/heartbeats")
async def get_heartbeats(user = lead_above):
    """Retrieves the last seen status for all devices.

    Args:
        user: Authorized lead user dependency.

    Returns:
        list: A list of device status objects including last seen time.
    """
    from precognito.ingestion.heartbeat import device_status
    
    results = []
    for device_id, last_seen in device_status.items():
        # Ensure timezone comparison works
        now = datetime.now(timezone.utc)
        ls = last_seen.replace(tzinfo=timezone.utc) if last_seen.tzinfo is None else last_seen
        diff = (now - ls).seconds
        status = "Active" if diff <= 5 else "Inactive"
        results.append({
            "deviceId": device_id,
            "lastSeen": last_seen.isoformat(),
            "status": status,
            "secondsSinceLast": diff
        })
    return results
