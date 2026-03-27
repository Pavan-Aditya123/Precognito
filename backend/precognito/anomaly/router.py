"""
FastAPI Router for Anomaly Detection Engine
Integrates with existing backend structure
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging
from datetime import datetime

from detector import detect_anomaly, detect_anomalies_batch, get_detector
from model import AnomalyDetectionModel

# Create router
router = APIRouter(
    prefix="/anomaly",
    tags=["Anomaly Detection"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models
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

# Setup logging
logger = logging.getLogger(__name__)

@router.get("/", summary="Anomaly Detection Health Check")
async def root():
    """Root endpoint for anomaly detection service"""
    return {
        "service": "Anomaly Detection API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@router.post("/detect", response_model=AnomalyResponse, summary="Detect Anomalies")
async def detect_single_anomaly(sensor_data: SensorData):
    """
    Detect anomalies in a single sensor reading
    
    - **machine_id**: Required - Machine identifier
    - **temperature**: Optional - Temperature in Kelvin
    - **vibration**: Optional - Vibration in mm/s  
    - **torque**: Optional - Torque in Nm
    - **tool_wear**: Optional - Tool wear in minutes
    """
    try:
        data_dict = sensor_data.dict(exclude_unset=True)
        result = detect_anomaly(data_dict)
        return AnomalyResponse(**result)
        
    except Exception as e:
        logger.error(f"Anomaly detection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@router.post("/detect/batch", response_model=List[AnomalyResponse], summary="Batch Anomaly Detection")
async def detect_batch_anomalies(batch_data: BatchSensorData):
    """Detect anomalies in multiple sensor readings"""
    try:
        data_list = [item.dict(exclude_unset=True) for item in batch_data.data]
        results = detect_anomalies_batch(data_list)
        return [AnomalyResponse(**result) for result in results]
        
    except Exception as e:
        logger.error(f"Batch anomaly detection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch detection failed: {str(e)}")

@router.get("/status", summary="System Status")
async def get_detector_status():
    """Get the current status of the anomaly detector"""
    try:
        detector = get_detector()
        status = detector.get_detector_status()
        return status
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.post("/train", summary="Train Model")
async def train_model():
    """Train/retrain the anomaly detection model"""
    try:
        trainer = AnomalyDetectionModel()
        results = trainer.train_and_evaluate()
        
        return {
            "success": True,
            "message": "Model training completed successfully",
            "training_time": results['training']['training_time'],
            "accuracy": results['evaluation']['metrics']['accuracy'],
            "f1_score": results['evaluation']['metrics']['f1_score']
        }
        
    except Exception as e:
        logger.error(f"Model training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.get("/simulate", summary="Test Simulation")
async def simulate_anomalies():
    """Run anomaly detection simulation with test cases"""
    try:
        detector = get_detector()
        
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
