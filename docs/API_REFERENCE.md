# Precognito: API Reference Guide

This document provides a technical reference for the Precognito REST API. The API is built with FastAPI and follows RESTful principles.

**Note**: Interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

---

## 🔐 Authentication

All API requests (except `/health` and `/docs`) require authentication. 
- **Session Auth**: Used by the web frontend via the `better-auth.session_token` cookie.
- **Bearer Auth**: Used by external tools or scripts. 
  ```http
  Authorization: Bearer <your_session_token>
  ```

---

## 🏥 System Endpoints

### `GET /health`
Returns the status of the API and its dependent services (PostgreSQL, InfluxDB).
- **Response**: `200 OK` (Healthy) or `503 Service Unavailable` (Degraded).

---

## 🏭 Asset & Telemetry Endpoints

### `GET /assets`
Retrieves all assets with their health status and last seen timestamp.
- **Query Parameters**:
  - `limit` (int, default: 100)
  - `offset` (int, default: 0)
- **Role Required**: `TECHNICIAN` and above.

### `GET /anomalies`
Fetches recently detected anomalies from InfluxDB.
- **Query Parameters**:
  - `limit` (int, default: 100)
  - `offset` (int, default: 0)
- **Role Required**: `OT_SPECIALIST` and above.

### `POST /ingest/dev`
Submit telemetry data directly for testing or simulation.
- **Payload**:
  ```json
  {
    "device_id": "motor_1",
    "temperature": 45.2,
    "vibration": 0.05
  }
  ```
- **Role Required**: `ADMIN`.

---

## 📋 Work Order Endpoints

### `POST /work-orders/assets/`
Create a new industrial asset.
- **Role Required**: `MANAGER`.

### `POST /work-orders/audit/`
Create a new manual work order (audit).
- **Role Required**: `MANAGER`.

### `PATCH /work-orders/audit/{id}/complete`
Mark a work order as completed and calculate final costs.
- **Role Required**: `MANAGER`.

---

## 📦 Inventory Endpoints

### `GET /inventory/`
List current spare parts stock levels.
- **Role Required**: `STORE_MANAGER` and above.

### `POST /inventory/reserve`
Reserve a part for an active work order.
- **Role Required**: `STORE_MANAGER` and above.

---

## 📊 Analytics & Financial Endpoints

### `GET /admin-reporting/recommendations`
Fetch AI-driven maintenance recommendations with ROI analysis.
- **Role Required**: `MANAGER`.

### `GET /analytics/metrics`
Retrieve ML model performance metrics (Precision, Recall, F1).
- **Role Required**: `OT_SPECIALIST` and above.

---

## ⚠️ Error Codes

| Status | Meaning | Description |
|--------|---------|-------------|
| 401 | Unauthorized | Missing or invalid authentication token. |
| 403 | Forbidden | User role does not have permission for this resource. |
| 422 | Unprocessable Entity | Validation error (e.g., missing required fields). |
| 429 | Too Many Requests | Rate limit exceeded. |
| 503 | Service Unavailable | Database or InfluxDB connection failure. |
