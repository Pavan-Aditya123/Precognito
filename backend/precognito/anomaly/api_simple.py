"""
Simplified FastAPI router for anomaly detection
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from core import AnomalyDetector

# Create router
router = APIRouter(prefix="/anomaly", tags=["Anomaly Detection"])

# Pydantic models
class SensorData(BaseModel):
    """Pydantic model for individual sensor telemetry.

    Attributes:
        machine_id: Unique identifier of the machine.
        temperature: Optional temperature reading in Kelvin.
        vibration: Optional vibration reading.
        torque: Optional torque reading in Nm.
    """
    machine_id: str
    temperature: Optional[float] = None
    vibration: Optional[float] = None
    torque: Optional[float] = None

class BatchSensorData(BaseModel):
    """Pydantic model for batch sensor telemetry.

    Attributes:
        data: List of SensorData objects.
    """
    data: List[SensorData]

class AnomalyResponse(BaseModel):
    """Pydantic model for anomaly detection response.

    Attributes:
        machine_id: Unique identifier of the machine.
        timestamp: ISO format timestamp of the detection.
        anomaly_detected: Boolean flag indicating if an anomaly was detected.
        anomaly_types: List of detected anomaly types (e.g., sensor names).
        severity: Classification of anomaly severity (LOW, MODERATE, HIGH, CRITICAL).
        confidence: Numerical confidence score of the detection.
        metrics: Dictionary of sensor metrics analyzed.
        reason: Explanation of the detection result.
    """
    machine_id: str
    timestamp: str
    anomaly_detected: bool
    anomaly_types: List[str]
    severity: str
    confidence: float
    metrics: Dict[str, float]
    reason: str

# Global detector
_detector = None

def get_detector_instance():
    """Initializes or retrieves the global AnomalyDetector instance.

    Returns:
        AnomalyDetector: The singleton anomaly detector instance.
    """
    global _detector
    if _detector is None:
        _detector = AnomalyDetector()
    return _detector

@router.get("/")
async def root():
    """Root endpoint for the Anomaly Detection API.

    Returns:
        dict: Service name and version.
    """
    return {"service": "Anomaly Detection API", "version": "2.0"}

@router.post("/detect", response_model=AnomalyResponse)
async def detect_anomaly(sensor_data: SensorData):
    """Detects anomalies for a single sensor reading.

    Args:
        sensor_data: Sensor telemetry data.

    Returns:
        AnomalyResponse: Detailed anomaly detection results.

    Raises:
        HTTPException: If an error occurs during detection.
    """
    try:
        detector = get_detector_instance()
        result = detector.detect_anomaly(sensor_data.dict())
        return AnomalyResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect/batch", response_model=List[AnomalyResponse])
async def detect_batch_anomalies(batch_data: BatchSensorData):
    """Detects anomalies for multiple sensor readings.

    Args:
        batch_data: Batch of sensor telemetry data.

    Returns:
        List[AnomalyResponse]: List of detailed anomaly detection results.

    Raises:
        HTTPException: If an error occurs during batch detection.
    """
    try:
        detector = get_detector_instance()
        data_list = [item.dict() for item in batch_data.data]
        results = detector.detect_batch(data_list)
        return [AnomalyResponse(**result) for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{machine_id}")
async def get_machine_history(machine_id: str):
    """Retrieves the rolling window history for a specific machine.

    Args:
        machine_id: Unique identifier of the machine.

    Returns:
        dict: Historical sensor data for the machine.

    Raises:
        HTTPException: If history retrieval fails.
    """
    try:
        detector = get_detector_instance()
        history = detector.get_history(machine_id)
        return {"machine_id": machine_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics/{machine_id}")
async def get_machine_statistics(machine_id: str):
    """Retrieves statistical analysis for a specific machine's sensor history.

    Args:
        machine_id: Unique identifier of the machine.

    Returns:
        dict: Statistical metrics for the machine's sensors.

    Raises:
        HTTPException: If statistics calculation fails.
    """
    try:
        detector = get_detector_instance()
        stats = detector.get_statistics(machine_id)
        return {"machine_id": machine_id, "statistics": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_status():
    """Retrieves the current status of the anomaly detection service.

    Returns:
        dict: Initialization status, model loading status, and tracked machine IDs.
    """
    detector = get_detector_instance()
    return {
        "initialized": detector.initialized,
        "model_loaded": detector.model is not None,
        "supported_sensors": list(detector.pattern_detector.history.keys())
    }
