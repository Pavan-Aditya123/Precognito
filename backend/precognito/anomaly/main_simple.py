"""
Simplified FastAPI application for anomaly detection
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api_simple import router

# Create app
app = FastAPI(
    title="Anomaly Detection API",
    description="Simplified pattern-based anomaly detection",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint for the Anomaly Detection application.

    Returns:
        dict: A welcome message and link to the API documentation.
    """
    return {"message": "Anomaly Detection API v2.0", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
