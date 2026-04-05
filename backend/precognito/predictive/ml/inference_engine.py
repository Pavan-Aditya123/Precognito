import os
import joblib
import pandas as pd
import numpy as np

class PredictiveInferenceEngine:
    """Engine for performing machine health predictive inference.

    This engine leverages trained machine learning models and scalers to predict
    the Remaining Useful Life (RUL) and identify potential fault types for machines
    based on incoming telemetry data.
    """

    def __init__(self, model_dir="models"):
        """Initializes the engine by loading pre-trained models and scalers.

        Args:
            model_dir: Path to the directory containing 'scaler.joblib',
                'rul_model.joblib', and 'fault_model.joblib'. Defaults to "models".
        """
        # Load the saved models
        self.scaler = joblib.load(os.path.join(model_dir, "scaler.joblib"))
        self.rul_model = joblib.load(os.path.join(model_dir, "rul_model.joblib"))
        self.fault_model = joblib.load(os.path.join(model_dir, "fault_model.joblib"))
    
    def predict(self, telemetry_data: dict) -> dict:
        """Predicts machine health metrics from telemetry data.

        Args:
            telemetry_data: A dictionary containing machine telemetry features:
                - vibration_rms
                - temperature
                - freq_spike_1x
                - freq_spike_bpfo

        Returns:
            A dictionary containing the prediction results:
                - predicted_rul_hours: Estimated RUL in hours.
                - predicted_fault_type: Most likely fault type.
                - confidence_score_percent: Confidence in the fault prediction.
                - risk_level: Risk level (Normal, Warning, High-Risk).
                - recommendation: Recommended maintenance action.
        """
        features = ["vibration_rms", "temperature", "freq_spike_1x", "freq_spike_bpfo"]
        
        # Verify columns exist or fill a default (e.g., 0)
        df_row = {}
        for f in features:
            df_row[f] = telemetry_data.get(f, 0.0)
            
        df = pd.DataFrame([df_row])
        
        # Scale
        X_scaled = self.scaler.transform(df)
        
        # Predict RUL
        # Predict RUL (undo the cuberoot linearization used during training for >95% accuracy)
        rul_pred = max(0, float(self.rul_model.predict(X_scaled)[0]) ** 3.0)
        
        # Predict Fault
        fault_pred = self.fault_model.predict(X_scaled)[0]
        # Predict Probabilities to extract confidence
        fault_probs = self.fault_model.predict_proba(X_scaled)[0]
        
        # Calculate Confidence Score (percentage of classification confidence)
        confidence = np.max(fault_probs) * 100.0
        
        # Planning Support / Risk Level Thresholding (TC_M3_05)
        # RUL value falls below defined threshold (< 48 hours)
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
