"""
FastAPI endpoints for Anomaly Detection Engine
Integrates with Swagger/OpenAPI for REST API access
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging
from datetime import datetime

from detector import detect_anomaly, detect_anomalies_batch, get_detector
from model import AnomalyDetectionModel

# Initialize FastAPI app
app = FastAPI(
    title="Anomaly Detection API",
    description="Production-ready anomaly detection for predictive maintenance",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class SensorData(BaseModel):
    machine_id: str = Field(..., description="Unique machine identifier")
    temperature: Optional[float] = Field(None, description="Temperature in Kelvin")
    vibration: Optional[float] = Field(None, description="Vibration in mm/s")
    torque: Optional[float] = Field(None, description="Torque in Nm")
    tool_wear: Optional[float] = Field(None, description="Tool wear in minutes")

class BatchSensorData(BaseModel):
    data: List[SensorData] = Field(..., description="List of sensor readings")

class AnomalyResponse(BaseModel):
    machine_id: str
    timestamp: str
    anomaly_detected: bool
    anomaly_types: List[str]
    severity: str
    confidence: float
    metrics: Dict[str, float]
    error: Optional[str] = None

class ModelTrainingResponse(BaseModel):
    success: bool
    message: str
    training_time: Optional[float] = None
    accuracy: Optional[float] = None
    f1_score: Optional[float] = None

class DetectorStatusResponse(BaseModel):
    initialized: bool
    model_loaded: bool
    scaler_loaded: bool
    feature_stats_loaded: bool
    supported_sensors: List[str]

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Anomaly Detection API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    try:
        detector = get_detector()
        status = detector.get_detector_status()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "detector": status
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.post("/detect", response_model=AnomalyResponse, tags=["Anomaly Detection"])
async def detect_single_anomaly(sensor_data: SensorData):
    """
    Detect anomalies in a single sensor reading
    
    - **machine_id**: Required - Machine identifier
    - **temperature**: Optional - Temperature in Kelvin
    - **vibration**: Optional - Vibration in mm/s  
    - **torque**: Optional - Torque in Nm
    - **tool_wear**: Optional - Tool wear in minutes
    
    Returns structured anomaly detection result with severity classification.
    """
    try:
        # Convert to dict for detector
        data_dict = sensor_data.dict(exclude_unset=True)
        
        # Perform anomaly detection
        result = detect_anomaly(data_dict)
        
        return AnomalyResponse(**result)
        
    except Exception as e:
        logger.error(f"Anomaly detection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.post("/detect/batch", response_model=List[AnomalyResponse], tags=["Anomaly Detection"])
async def detect_batch_anomalies(batch_data: BatchSensorData):
    """
    Detect anomalies in multiple sensor readings
    
    - **data**: List of sensor data objects
    
    Returns list of anomaly detection results for each reading.
    """
    try:
        # Convert to list of dicts
        data_list = [item.dict(exclude_unset=True) for item in batch_data.data]
        
        # Perform batch detection
        results = detect_anomalies_batch(data_list)
        
        return [AnomalyResponse(**result) for result in results]
        
    except Exception as e:
        logger.error(f"Batch anomaly detection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch detection failed: {str(e)}")

@app.get("/status", response_model=DetectorStatusResponse, tags=["System"])
async def get_detector_status():
    """
    Get the current status of the anomaly detector
    
    Returns initialization status and system information.
    """
    try:
        detector = get_detector()
        status = detector.get_detector_status()
        return DetectorStatusResponse(**status)
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.post("/train", response_model=ModelTrainingResponse, tags=["Model Training"])
async def train_model():
    """
    Train/retrain the anomaly detection model
    
    Trains the Isolation Forest model on the historical data.
    This may take a few seconds to complete.
    """
    try:
        trainer = AnomalyDetectionModel()
        results = trainer.train_and_evaluate()
        
        return ModelTrainingResponse(
            success=True,
            message="Model training completed successfully",
            training_time=results['training']['training_time'],
            accuracy=results['evaluation']['metrics']['accuracy'],
            f1_score=results['evaluation']['metrics']['f1_score']
        )
        
    except Exception as e:
        logger.error(f"Model training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/simulate", response_model=Dict, tags=["Testing"])
async def simulate_anomalies():
    """
    Simulate anomaly detection with test cases
    
    Runs the detection system through various test scenarios
    including normal operation and different anomaly types.
    """
    try:
        detector = get_detector()
        
        # Test cases
        test_data = {
            "machine_id": "SIM_TEST",
            "temperature": 305.0,
            "vibration": 1500.0,
            "torque": 45.0
        }
        
        simulation_result = detector.simulate_anomaly_detection(test_data)
        return simulation_result
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.get("/metrics", tags=["System"])
async def get_system_metrics():
    """
    Get system performance metrics
    
    Returns performance statistics and model information.
    """
    try:
        detector = get_detector()
        
        # Get model info
        model_info = detector.get_detector_status()
        
        # Calculate some basic metrics
        import time
        import psutil
        import os
        
        start_time = time.time()
        test_data = {
            "machine_id": "METRIC_TEST",
            "temperature": 300.0,
            "vibration": 1500.0,
            "torque": 40.0
        }
        
        # Measure detection performance
        detect_anomaly(test_data)
        detection_time = (time.time() - start_time) * 1000  # ms
        
        # System metrics
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        return {
            "performance": {
                "detection_time_ms": round(detection_time, 2),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2)
            },
            "model": model_info,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Metrics failed: {str(e)}")

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")

if __name__ == "__main__":
    import uvicorn
    
    # Run the FastAPI app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
