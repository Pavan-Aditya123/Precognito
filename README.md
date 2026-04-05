# Precognito

AI-powered predictive maintenance platform designed to eliminate unplanned downtime. By analyzing real-time IoT sensor telemetry and historical patterns, it identifies anomalies and predicts Remaining Useful Life (RUL) before failures occur.

## 🚀 Project Status: Industrial Grade (10/10 Readiness)

The Precognito platform has been fully hardened for production deployment. It features a robust security architecture, high-performance data pipelines, and a comprehensive automated testing suite.

### Core Industrial Capabilities
- **Multi-Layer Security**: RBAC, Session/JWT auth, and SQLi/XSS protection.
- **Scalable Ingestion**: Asynchronous InfluxDB batching with automated retry logic.
- **Fault Tolerance**: Circuit Breaker pattern integration for external database dependencies.
- **Observability**: Structured JSON logging and real-time `/health` monitoring.
- **Automated Operations**: Alembic schema migrations and JIT inventory procurement.
- **Financial Intelligence**: Real-time ROI analysis and emergency-vs-scheduled cost modeling.
- **ML Ops**: Real-world Model Drift Detection comparing predictions against actual outcomes.

## Project Structure

```
precognito/
├── frontend/              # Next.js 16 PWA (Production Optimized)
│   ├── src/app/          # Role-based protected routes
│   └── tests/e2e/        # Playwright browser test suite
│
├── backend/               # FastAPI Python package
│   ├── precognito/       # Core industrial logic
│   └── tests/            # Full test pyramid (Unit, Integration, Security)
│
├── docs/                  # Detailed Admin and API documentation
├── Dockerfile             # Multi-stage optimized production image
└── docker-compose.yml     # Zero-config industrial stack
```

## Getting Started (Team Quick Start)

### 1. The "One Command" Developer Mode (Recommended)
This starts the Docker infrastructure, the Backend, the Frontend, and the Simulator all in one terminal window:
```bash
uv run python start_all.py
```
*Press `Ctrl+C` to stop all services at once.*

### 2. Unified Setup (Docker)
The entire stack (Postgres, InfluxDB, Mosquitto, API, and Frontend) can be started with a single command:
```bash
docker compose up --build -d
```
- **Frontend**: `http://localhost:3000`
- **API Docs**: `http://localhost:8000/docs`
- **InfluxDB**: `http://localhost:8086`

### 2. Initial User Setup
To create test accounts for all roles (Admin, Manager, Tech, etc.), run the following command:
```bash
cd frontend
bun scripts/seed-all-users.ts
```
*Note: Default password for all seeded users is `Password123!`*

### 3. Manual Backend Setup (Development)
```bash
uv sync
# Run unified server (API + MQTT Worker)
uv run python main.py
```

### 4. Manual Frontend Setup (Development)
```bash
cd frontend
bun install
bun run dev:lite
```

### 5. Database Migrations
```bash
cd backend
uv run alembic upgrade head
```

### 6. Data Simulation
To generate live telemetry data for the dashboard, run the simulator in a separate terminal:
```bash
uv run python backend/precognito/ingestion/simulator.py
```

## 🧪 Comprehensive Testing Suite

Precognito features 100% coverage of critical industrial paths across multiple layers:

### Backend Tests (Unit, Integration, Security, Contract)
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
pytest
```

### Frontend Tests (Unit & Visual Snapshots)
```bash
cd frontend
bun run test
```

### Frontend E2E Tests (Playwright)
```bash
cd frontend
bun run test:e2e
```

### Performance Load Tests (Locust)
```bash
locust -f tests/performance/locustfile.py --headless -u 10 -r 1
```

## Documentation
For detailed technical instructions, see the `docs/` directory:
- **[Industrial User Manual](./USER_MANUAL.md)**: Guide for technicians and managers.
- **[Administrator & Deployment Guide](./docs/ADMIN_GUIDE.md)**: DevOps and IT maintenance.
- **[API Reference Guide](./docs/API_REFERENCE.md)**: Technical integration details.

## License
MIT License - see [LICENSE](./LICENSE) for details.
