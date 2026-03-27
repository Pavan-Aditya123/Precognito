"""
Utility functions for Anomaly Detection Engine
Contains helper functions for logging, validation, and common operations
"""

import logging
import pickle
import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import time

from config import SEVERITY_THRESHOLDS, SENSOR_CONFIG

def setup_logging(log_level: str = "INFO", log_format: str = None) -> logging.Logger:
    """Setup logging configuration"""
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("anomaly_detection.log")
        ]
    )
    
    return logging.getLogger(__name__)

def save_model(model, scaler, file_path: str, scaler_path: str) -> bool:
    """Save trained model and scaler to disk"""
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        
        logging.info(f"Model saved to {file_path}")
        logging.info(f"Scaler saved to {scaler_path}")
        return True
    except Exception as e:
        logging.error(f"Error saving model: {e}")
        return False

def load_model(file_path: str, scaler_path: str) -> Tuple[Any, Any]:
    """Load trained model and scaler from disk"""
    try:
        with open(file_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        logging.info(f"Model loaded from {file_path}")
        logging.info(f"Scaler loaded from {scaler_path}")
        return model, scaler
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None, None

def validate_input_data(data: Dict) -> Tuple[bool, str]:
    """Validate input data format and values"""
    required_fields = ["machine_id"]
    sensor_fields = ["temperature", "vibration", "torque"]
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Check at least one sensor field
    has_sensor = any(field in data for field in sensor_fields)
    if not has_sensor:
        return False, "At least one sensor field (temperature, vibration, torque) is required"
    
    # Validate numeric values
    for field in sensor_fields:
        if field in data:
            try:
                value = float(data[field])
                if value < 0:
                    return False, f"{field} cannot be negative"
            except (ValueError, TypeError):
                return False, f"{field} must be a numeric value"
    
    return True, "Valid input"

def calculate_severity(anomaly_score: float) -> str:
    """Calculate severity level based on anomaly score"""
    if anomaly_score >= SEVERITY_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    elif anomaly_score >= SEVERITY_THRESHOLDS["HIGH"]:
        return "HIGH"
    elif anomaly_score >= SEVERITY_THRESHOLDS["MODERATE"]:
        return "MODERATE"
    elif anomaly_score >= SEVERITY_THRESHOLDS["LOW"]:
        return "LOW"
    else:
        return "NORMAL"

def calculate_confidence(anomaly_score: float, model_prediction: float) -> float:
    """Calculate confidence score for anomaly detection"""
    # Combine anomaly score with model prediction
    base_confidence = abs(anomaly_score)
    model_confidence = abs(model_prediction)
    
    # Weighted average
    confidence = (base_confidence * 0.6 + model_confidence * 0.4)
    
    # Ensure confidence is between 0 and 1
    confidence = min(max(confidence, 0.0), 1.0)
    
    return round(confidence, 3)

def identify_anomaly_types(data: Dict, feature_stats: Dict) -> List[str]:
    """Identify which sensor readings are causing anomalies"""
    anomaly_types = []
    
    for sensor_name, sensor_config in SENSOR_CONFIG.items():
        if sensor_name in data:
            value = float(data[sensor_name])
            column_name = sensor_config["column"]
            
            if column_name in feature_stats:
                stats = feature_stats[column_name]
                mean = stats["mean"]
                std = stats["std"]
                
                # Calculate z-score
                z_score = abs((value - mean) / std) if std > 0 else 0
                
                # If z-score is high, consider it anomalous
                if z_score > 4.0:
                    anomaly_types.append(sensor_name)
    
    return anomaly_types

def format_output(
    machine_id: str,
    anomaly_detected: bool,
    anomaly_score: float,
    model_prediction: float,
    anomaly_types: List[str],
    metrics: Dict,
    timestamp: Optional[str] = None
) -> Dict:
    """Format the final output in the required JSON structure"""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    if not anomaly_detected:
        severity = "LOW"
    elif anomaly_score > 0.8:
        severity = "HIGH"
    elif anomaly_score > 0.6:
        severity = "MODERATE"
    else:
        severity = "LOW"
    confidence = calculate_confidence(anomaly_score, model_prediction)
    
    output = {
        "machine_id": machine_id,
        "timestamp": timestamp,
        "anomaly_detected": anomaly_detected,
        "anomaly_types": anomaly_types,
        "severity": severity,
        "confidence": confidence,
        "metrics": metrics
    }
    
    return output

def calculate_anomaly_score(data: Dict, feature_stats: Dict, model_prediction: float) -> float:
    """Calculate comprehensive anomaly score combining statistical and ML methods"""
    total_score = 0.0
    weight_sum = 0.0
    
    for sensor_name, sensor_config in SENSOR_CONFIG.items():
        if sensor_name in data:
            value = float(data[sensor_name])
            column_name = sensor_config["column"]
            weight = sensor_config["weight"]
            
            if column_name in feature_stats:
                stats = feature_stats[column_name]
                mean = stats["mean"]
                std = stats["std"]
                
                # Calculate z-score
                z_score = abs((value - mean) / std) if std > 0 else 0
                
                # Normalize z-score to 0-1 range (capping at 3 sigma)
                normalized_score = min(z_score / 3.0, 1.0)
                
                total_score += normalized_score * weight
                weight_sum += weight
    
    # Combine statistical score with ML prediction
    if weight_sum > 0:
        statistical_score = total_score / weight_sum
        combined_score = (statistical_score * 0.5 + abs(model_prediction) * 0.5)
    else:
        combined_score = abs(model_prediction)
    
    return round(combined_score, 3)

def check_performance_constraints(start_time: float) -> bool:
    """Check if detection is within performance constraints"""
    elapsed_time = time.time() - start_time
    max_latency = 2.0  # seconds
    
    if elapsed_time > max_latency:
        logging.warning(f"Detection latency {elapsed_time:.2f}s exceeds maximum {max_latency}s")
        return False
    
    return True

def create_error_response(machine_id: str, error_message: str) -> Dict:
    """Create standardized error response"""
    return {
        "machine_id": machine_id,
        "timestamp": datetime.now().isoformat(),
        "anomaly_detected": False,
        "anomaly_types": [],
        "severity": "ERROR",
        "confidence": 0.0,
        "metrics": {},
        "error": error_message
    }

def log_detection_result(result: Dict) -> None:
    """Log detection result for monitoring"""
    log_message = (
        f"Detection for {result['machine_id']}: "
        f"Anomaly={result['anomaly_detected']}, "
        f"Severity={result['severity']}, "
        f"Confidence={result['confidence']}"
    )
    
    if result['anomaly_detected']:
        logging.warning(log_message)
    else:
        logging.info(log_message)

def batch_process_data(data_list: List[Dict], detector_instance) -> List[Dict]:
    """Process multiple data points in batch"""
    results = []
    
    for data in data_list:
        try:
            result = detector_instance.detect_anomaly(data)
            results.append(result)
        except Exception as e:
            error_result = create_error_response(
                data.get('machine_id', 'unknown'),
                str(e)
            )
            results.append(error_result)
    
    return results

def export_results(results: List[Dict], file_path: str) -> bool:
    """Export detection results to file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logging.info(f"Results exported to {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error exporting results: {e}")
        return False

def calculate_model_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
    """Calculate model performance metrics"""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    try:
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
            "recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
            "f1_score": f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }
        
        return metrics
    except Exception as e:
        logging.error(f"Error calculating metrics: {e}")
        return {}
