"""
Real-time anomaly detection module for Predictive Maintenance System
Handles real-time detection, severity classification, and response formatting
"""

import numpy as np
import pandas as pd
import time
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from config import MODEL_PATH, SCALER_PATH, SENSOR_CONFIG
from preprocessing import DataPreprocessor
from utils import (
    setup_logging, load_model, validate_input_data, format_output,
    calculate_anomaly_score, identify_anomaly_types, check_performance_constraints,
    create_error_response, log_detection_result, batch_process_data
)

class AnomalyDetector:
    """Main class for real-time anomaly detection"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.preprocessor = DataPreprocessor()
        self.model = None
        self.feature_stats = {}
        self.feature_names = []
        self.is_initialized = False
        
        # Try to load existing model
        self._initialize()
    
    def _initialize(self) -> bool:
        """Initialize the detector with trained model"""
        try:
            # Load model and scaler
            self.model, self.preprocessor.scaler = load_model(MODEL_PATH, SCALER_PATH)
            
            if self.model is None:
                self.logger.error("Failed to load model. Please train the model first.")
                return False
            
            # Load feature statistics
            stats_path = MODEL_PATH.parent / "feature_stats.json"
            if stats_path.exists():
                with open(stats_path, 'r') as f:
                    self.feature_stats = json.load(f)
            
            # Load feature names
            names_path = MODEL_PATH.parent / "feature_names.json"
            if names_path.exists():
                with open(names_path, 'r') as f:
                    self.feature_names = json.load(f)
            
            self.is_initialized = True
            self.logger.info("Anomaly detector initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing detector: {e}")
            return False
    
    def detect_anomaly(self, data: Dict) -> Dict:
        """
        Detect anomalies in real-time sensor data
        
        Args:
            data: Dictionary containing sensor readings
                  {
                      "machine_id": "M1",
                      "temperature": 90.0,
                      "vibration": 6.5,
                      "torque": 45.0
                  }
        
        Returns:
            Formatted JSON response with anomaly detection results
        """
        start_time = time.time()
        
        try:
            # Validate input
            is_valid, error_message = validate_input_data(data)
            if not is_valid:
                return create_error_response(data.get('machine_id', 'unknown'), error_message)
            
            # Check if detector is initialized
            if not self.is_initialized:
                return create_error_response(
                    data['machine_id'], 
                    "Detector not initialized. Please train the model first."
                )
            
            # Preprocess input data
            features = self.preprocessor.preprocess_for_prediction(data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            # Convert to anomaly score: -1 (anomaly) -> 1, 1 (normal) -> 0
            model_prediction = 1 if prediction == -1 else 0
            
            # Get anomaly score (decision function)
            if hasattr(self.model, 'decision_function'):
                anomaly_score_raw = self.model.decision_function(features)[0]
                # Normalize to 0-1 range
                anomaly_score = max(0, min(1, -anomaly_score_raw))
            else:
                anomaly_score = float(model_prediction)
            
            # Calculate comprehensive anomaly score
            comprehensive_score = calculate_anomaly_score(data, self.feature_stats, anomaly_score)
            
            # Identify anomaly types
           # Determine if anomaly is detected
            anomaly_detected = (comprehensive_score > 0.3)

            # Identify anomaly types
            if anomaly_detected:
                anomaly_types = identify_anomaly_types(data, self.feature_stats)
    
                # Safety: if no strong anomaly types → treat as normal
                if not anomaly_types:
                    anomaly_detected = False
            else:
                anomaly_types = []  
            
            # Prepare metrics
            metrics = {}
            for sensor in SENSOR_CONFIG.keys():
                if sensor in data:
                    metrics[sensor] = float(data[sensor])
            
            # Format output
            result = format_output(
                machine_id=data['machine_id'],
                anomaly_detected=anomaly_detected,
                anomaly_score=comprehensive_score,
                model_prediction=model_prediction,
                anomaly_types=anomaly_types,
                metrics=metrics
            )
            
            # Check performance constraints
            performance_ok = check_performance_constraints(start_time)
            if not performance_ok:
                result['performance_warning'] = "Detection latency exceeded 2 seconds"
            
            # Log result
            log_detection_result(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in anomaly detection: {e}")
            return create_error_response(data.get('machine_id', 'unknown'), str(e))
    
    def detect_anomalies_batch(self, data_list: List[Dict]) -> List[Dict]:
        """
        Detect anomalies in multiple data points
        
        Args:
            data_list: List of sensor data dictionaries
        
        Returns:
            List of anomaly detection results
        """
        self.logger.info(f"Processing batch of {len(data_list)} data points")
        return batch_process_data(data_list, self)
    
    def get_detector_status(self) -> Dict:
        """Get the current status of the anomaly detector"""
        status = {
            "initialized": self.is_initialized,
            "model_loaded": self.model is not None,
            "scaler_loaded": self.preprocessor.scaler is not None,
            "feature_stats_loaded": len(self.feature_stats) > 0,
            "model_path": str(MODEL_PATH),
            "scaler_path": str(SCALER_PATH),
            "supported_sensors": list(SENSOR_CONFIG.keys())
        }
        
        if self.is_initialized:
            status["model_info"] = {
                "type": "Isolation Forest",
                "n_features": len(self.feature_names),
                "feature_names": self.feature_names[:10]  # Show first 10 features
            }
        
        return status
    
    def update_thresholds(self, new_thresholds: Dict) -> bool:
        """Update anomaly detection thresholds"""
        try:
            # This would update the severity thresholds
            # For now, just log the request
            self.logger.info(f"Threshold update requested: {new_thresholds}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating thresholds: {e}")
            return False
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance information"""
        if not self.is_initialized or self.model is None:
            return {"error": "Model not loaded"}
        
        # For Isolation Forest, we can get feature importance from the tree structure
        try:
            if hasattr(self.model, 'feature_importances_'):
                importance = self.model.feature_importances_
                feature_importance = {
                    self.feature_names[i]: float(importance[i])
                    for i in range(len(self.feature_names))
                }
                
                # Sort by importance
                sorted_features = sorted(
                    feature_importance.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                
                return {
                    "feature_importance": dict(sorted_features[:20]),  # Top 20
                    "total_features": len(self.feature_names)
                }
            else:
                return {"message": "Feature importance not available for this model"}
                
        except Exception as e:
            self.logger.error(f"Error getting feature importance: {e}")
            return {"error": str(e)}
    
    def simulate_anomaly_detection(self, test_data: Dict) -> Dict:
        """
        Simulate anomaly detection for testing purposes
        Creates synthetic anomalies based on input data
        """
        try:
            # Create variations of the input data
            test_cases = []
            
            # Normal case (original data)
            test_cases.append({
                "case": "normal",
                "data": test_data.copy()
            })
            
            # Temperature anomaly
            if "temperature" in test_data:
                temp_anomaly = test_data.copy()
                temp_anomaly["temperature"] = float(test_data["temperature"]) * 1.5
                test_cases.append({
                    "case": "temperature_anomaly",
                    "data": temp_anomaly
                })
            
            # Vibration anomaly
            if "vibration" in test_data:
                vib_anomaly = test_data.copy()
                vib_anomaly["vibration"] = float(test_data["vibration"]) * 2.0
                test_cases.append({
                    "case": "vibration_anomaly",
                    "data": vib_anomaly
                })
            
            # Multiple anomalies
            multi_anomaly = test_data.copy()
            if "temperature" in multi_anomaly:
                multi_anomaly["temperature"] = float(multi_anomaly["temperature"]) * 1.3
            if "vibration" in multi_anomaly:
                multi_anomaly["vibration"] = float(multi_anomaly["vibration"]) * 1.8
            test_cases.append({
                "case": "multiple_anomalies",
                "data": multi_anomaly
            })
            
            # Run detection on all test cases
            results = {}
            for test_case in test_cases:
                result = self.detect_anomaly(test_case["data"])
                results[test_case["case"]] = result
            
            return {
                "simulation_results": results,
                "test_data": test_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in anomaly simulation: {e}")
            return create_error_response("simulation", str(e))

# Global detector instance
_detector_instance = None

def get_detector() -> AnomalyDetector:
    """Get or create the global detector instance"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = AnomalyDetector()
    return _detector_instance

def detect_anomaly(data: Dict) -> Dict:
    """
    Convenience function for direct anomaly detection
    
    Args:
        data: Sensor data dictionary
    
    Returns:
        Formatted anomaly detection result
    """
    detector = get_detector()
    return detector.detect_anomaly(data)

def detect_anomalies_batch(data_list: List[Dict]) -> List[Dict]:
    """
    Convenience function for batch anomaly detection
    
    Args:
        data_list: List of sensor data dictionaries
    
    Returns:
        List of anomaly detection results
    """
    detector = get_detector()
    return detector.detect_anomalies_batch(data_list)

# Example usage and testing functions
def example_usage():
    """Example of how to use the anomaly detector"""
    # Sample data
    test_data = {
        "machine_id": "M1",
        "temperature": 305.0,
        "vibration": 1500.0,
        "torque": 45.0
    }
    
    # Get detector and detect anomalies
    detector = get_detector()
    result = detector.detect_anomaly(test_data)
    
    print("Anomaly Detection Result:")
    print(json.dumps(result, indent=2, default=str))
    
    # Run simulation
    sim_result = detector.simulate_anomaly_detection(test_data)
    print("\nSimulation Results:")
    print(json.dumps(sim_result, indent=2, default=str))

if __name__ == "__main__":
    example_usage()
