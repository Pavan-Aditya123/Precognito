"""
Main FastAPI application for Anomaly Detection
Standalone server for testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import the router
from router import router as anomaly_router

# Create FastAPI app
app = FastAPI(
    title="Anomaly Detection API",
    description="Production-ready anomaly detection for predictive maintenance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the anomaly router
app.include_router(anomaly_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Anomaly Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
