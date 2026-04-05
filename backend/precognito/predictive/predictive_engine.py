"""
Predictive maintenance engine for RUL and fault type prediction.
"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

class PredictiveInferenceEngine:
    """Engine for performing Remaining Useful Life (RUL) and fault type predictions.

    Attributes:
        scaler: Loaded MinMaxScaler for feature normalization.
        rul_model: Loaded regression model for RUL estimation.
        fault_model: Loaded classifier for fault type identification.
        initialized: Whether models were successfully loaded.
    """

    def __init__(self):
        """Initializes the engine and loads pre-trained models from the models directory.
        """
        # Resolve models directory relative to this file
        base_path = Path(__file__).parent
        model_dir = base_path / "models"
        
        try:
            self.scaler = joblib.load(model_dir / "scaler.joblib")
            self.rul_model = joblib.load(model_dir / "rul_model.joblib")
            self.fault_model = joblib.load(model_dir / "fault_model.joblib")
            self.initialized = True
        except Exception as e:
            print(f"Error loading predictive models: {e}")
            self.initialized = False
    
    def predict(self, telemetry_data: dict) -> dict:
        """Predicts RUL and fault type from telemetry data.

        Args:
            telemetry_data: Dictionary of sensor features (vibration_rms,
                temperature, freq_spike_1x, freq_spike_bpfo).

        Returns:
            A dictionary containing prediction results including:
                - predicted_rul_hours
                - predicted_fault_type
                - confidence_score_percent
                - risk_level
                - recommendation
        """
        if not self.initialized:
            return {
                "error": "Predictive engine not initialized",
                "predicted_rul_hours": 0.0,
                "predicted_fault_type": "Unknown",
                "confidence_score_percent": 0.0,
                "risk_level": "Unknown"
            }

        features = ["vibration_rms", "temperature", "freq_spike_1x", "freq_spike_bpfo"]
        
        # Verify columns exist or fill a default (e.g., 0)
        df_row = {}
        for f in features:
            df_row[f] = telemetry_data.get(f, 0.0)
            
        df = pd.DataFrame([df_row])
        
        try:
            # Scale
            X_scaled = self.scaler.transform(df)
            
            # Predict RUL (undo the cuberoot linearization used during training)
            rul_pred = max(0, float(self.rul_model.predict(X_scaled)[0]) ** 3.0)
            
            # Predict Fault
            fault_pred = self.fault_model.predict(X_scaled)[0]
            # Predict Probabilities to extract confidence
            fault_probs = self.fault_model.predict_proba(X_scaled)[0]
            
            # Calculate Confidence Score
            confidence = np.max(fault_probs) * 100.0
            
            # Planning Support / Risk Level Thresholding
            risk_level = "Normal"
            recommendation = "Continue Operation"
            if rul_pred < 48:
                risk_level = "High-Risk"
                recommendation = "Immediate Maintenance Required"
            elif rul_pred < 150:
                risk_level = "Warning"
                recommendation = "Schedule Maintenance"
                
            return {
                "predicted_rul_hours": round(float(rul_pred), 2),
                "predicted_fault_type": str(fault_pred),
                "confidence_score_percent": round(float(confidence), 2),
                "risk_level": risk_level,
                "recommendation": recommendation
            }
        except Exception as e:
            return {
                "error": f"Prediction failed: {str(e)}",
                "predicted_rul_hours": 0.0,
                "predicted_fault_type": "Unknown",
                "confidence_score_percent": 0.0,
                "risk_level": "Unknown"
            }

# Singleton instance
_engine = None

def get_predictive_engine():
    """Retrieves or initializes the global PredictiveInferenceEngine singleton.

    Returns:
        The PredictiveInferenceEngine singleton instance.
    """
    global _engine
    if _engine is None:
        _engine = PredictiveInferenceEngine()
    return _engine

def predict_rul(data: dict) -> dict:
    """Convenience wrapper for predicting machine health metrics.

    Args:
        data: Dictionary of machine telemetry features.

    Returns:
        A dictionary containing the predictive results.
    """
    return get_predictive_engine().predict(data)
