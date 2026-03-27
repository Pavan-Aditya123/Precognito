"""
Configuration file for Anomaly Detection Engine
Contains thresholds, model parameters, and system settings
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "predictive_maintenance.csv"
MODEL_PATH = BASE_DIR / "anomaly_model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"

# Sensor configuration
SENSOR_CONFIG = {
    "temperature": {
        "column": "Process temperature [K]",
        "unit": "K",
        "normal_min": 298.0,
        "normal_max": 310.0,
        "critical_threshold": 320.0,
        "weight": 0.4
    },
    "vibration": {
        "column": "Rotational speed [rpm]",
        "unit": "rpm",
        "normal_min": 1200.0,
        "normal_max": 1800.0,
        "critical_threshold": 2000.0,
        "weight": 0.6
    },
    "torque": {
        "column": "Torque [Nm]",
        "unit": "Nm",
        "normal_min": 20.0,
        "normal_max": 60.0,
        "critical_threshold": 80.0,
        "weight": 0.3
    }
}

# Anomaly detection thresholds
SEVERITY_THRESHOLDS = {
    "LOW": 0.1,
    "MODERATE": 0.25,
    "HIGH": 0.5,
    "CRITICAL": 0.75
}

# Model configuration
ISOLATION_FOREST_CONFIG = {
    "contamination": 0.1,  # Expected proportion of anomalies
    "random_state": 42,
    "n_estimators": 100,
    "max_samples": "auto"
}

# Preprocessing configuration
PREPROCESSING_CONFIG = {
    "rolling_window_size": 5,
    "smoothing_method": "rolling_mean",
    "fill_missing_method": "forward_fill",
    "scaling_method": "standard"
}

# Performance settings
MAX_DETECTION_LATENCY = 2.0  # seconds
BATCH_SIZE = 1000

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Feature engineering
FEATURE_COLUMNS = [
    "Process temperature [K]",
    "Rotational speed [rpm]", 
    "Torque [Nm]",
    "Tool wear [min]"
]

# Training configuration
TRAIN_TEST_SPLIT = 0.8
CROSS_VALIDATION_FOLDS = 5
