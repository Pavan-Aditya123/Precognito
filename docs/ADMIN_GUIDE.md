# Precognito: Administrator & Deployment Guide

This guide is intended for system administrators, DevOps engineers, and IT staff responsible for deploying, configuring, and maintaining the Precognito platform.

---

## 🏗 System Architecture

Precognito uses a modern microservices-inspired architecture:
- **Frontend**: Next.js 16 (React) PWA with Tailwind CSS.
- **Backend**: FastAPI (Python 3.12) handling core logic and API.
- **Primary Database**: PostgreSQL (Relational) for users, work orders, and inventory.
- **Telemetry Database**: InfluxDB 2.x (Time-series) for high-frequency sensor data.
- **IoT Broker**: Mosquitto (MQTT) for industrial data ingestion.
- **Worker**: Integrated MQTT worker for real-time DSP and ingestion.

---

## 🚀 Deployment

### 1. Prerequisites
- Docker and Docker Compose
- Node.js (Bun preferred)
- Python 3.12+ (uv preferred)

### 2. Environment Configuration
Create a `.env` file in the root directory based on `.env.example`. Key variables include:
- `DATABASE_URL`: PostgreSQL connection string.
- `INFLUX_TOKEN`: Authentication token for InfluxDB.
- `BETTER_AUTH_SECRET`: Secret key for authentication encryption.
- `ENFORCE_HTTPS`: Set to `True` in production.

### 3. Quick Start (Docker)
```bash
docker compose up -d
```
This will spin up Postgres, InfluxDB, and Mosquitto.

---

## 🔒 Security Management

### 1. User Roles & RBAC
Precognito enforces strict Role-Based Access Control (RBAC):
- **ADMIN**: Full system access, including audit logs and user management.
- **MANAGER**: Access to financial reports, recommendations, and inventory procurement.
- **STORE_MANAGER**: Specialized access for inventory and procurement flows.
- **OT_SPECIALIST**: Access to technical telemetry, safety alerts, and ML feedback.
- **TECHNICIAN**: Access to assigned work orders and QR check-ins.

### 2. Secrets Rotation
Rotate the following secrets quarterly:
- `BETTER_AUTH_SECRET` (Invalidates all active sessions)
- `INFLUX_TOKEN`
- PostgreSQL password

### 3. Network Security
- Ensure the API is behind a Load Balancer with TLS termination.
- Restrict MQTT access to authorized industrial gateways only.
- The system includes a **Circuit Breaker** pattern to protect against InfluxDB failures.

---

## 🛠 Maintenance & Operations

### 1. Database Migrations
The system uses **Alembic** for schema management.
```bash
cd backend
uv run alembic upgrade head
```

### 2. Observability
- **Logs**: Backend logs are output in structured JSON format to `stdout`.
- **Health Check**: Monitor the `/health` endpoint for real-time service status.
- **Performance**: Use the included **Locust** load tests (`tests/performance/`) to verify capacity before scaling.

### 3. Model Monitoring
- Run the **Drift Detector** script weekly to verify ML model accuracy:
```bash
python3 backend/precognito/predictive/drift_detector.py
```
- If Mean Absolute Error (MAE) exceeds 24 hours, initiate an XGBoost model retrain.

---

## 🚑 Troubleshooting

| Issue | Potential Cause | Resolution |
|-------|-----------------|------------|
| 503 Service Unavailable | DB or InfluxDB down | Check container status and `/health` endpoint. |
| 401 Unauthorized | Token expired | Re-authenticate via the login page. |
| Ingestion Lag | MQTT Broker overload | Scale Mosquitto or optimize DSP window in `preprocess.py`. |
| 403 Permission Denied | Insufficient Role | Verify user role in the PostgreSQL `user` table. |
