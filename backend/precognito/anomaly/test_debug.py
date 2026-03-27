"""
Debug script to test anomaly detection step by step
"""

import json
import pandas as pd
import numpy as np
from preprocessing import DataPreprocessor
from utils import load_model
from config import MODEL_PATH, SCALER_PATH

def debug_preprocessing():
    """Debug the preprocessing pipeline step by step"""
    print("=== Debugging Preprocessing Pipeline ===")
    
    # Load model and scaler
    model, scaler = load_model(MODEL_PATH, SCALER_PATH)
    
    # Load feature names
    with open(MODEL_PATH.parent / "feature_names.json", 'r') as f:
        feature_names = json.load(f)
    
    print(f"Expected feature names ({len(feature_names)}):")
    for i, name in enumerate(feature_names):
        print(f"  {i}: {name}")
    
    # Test data
    test_data = {
        "machine_id": "M1",
        "temperature": 305.0,
        "vibration": 1500.0,
        "torque": 45.0
    }
    
    print(f"\nTest data: {test_data}")
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    preprocessor.feature_names = feature_names
    preprocessor.scaler = scaler
    
    # Step by step preprocessing
    print("\n=== Step 1: Creating DataFrame ===")
    df = pd.DataFrame([test_data])
    print(f"DataFrame columns: {list(df.columns)}")
    print(f"DataFrame shape: {df.shape}")
    
    # Map columns
    column_mapping = {
        "temperature": "Process temperature [K]",
        "vibration": "Rotational speed [rpm]",
        "torque": "Torque [Nm]",
        "tool_wear": "Tool wear [min]",
        "air_temperature": "Air temperature [K]"
    }
    
    for key, col_name in column_mapping.items():
        if key in test_data and col_name not in df.columns:
            df[col_name] = test_data[key]
    
    print(f"After mapping columns: {list(df.columns)}")
    
    # Add missing columns
    default_values = {
        "Air temperature [K]": 298.0,
        "Process temperature [K]": 308.0,
        "Rotational speed [rpm]": 1500.0,
        "Torque [Nm]": 40.0,
        "Tool wear [min]": 0.0,
        "UDI": 1,
        "Product ID": "M14860",
        "Type": "M",
        "Target": 0,
        "Failure Type": "No Failure"
    }
    
    for col, default_val in default_values.items():
        if col not in df.columns:
            df[col] = default_val
    
    print(f"After adding defaults: {list(df.columns)}")
    
    # Clean data
    print("\n=== Step 2: Cleaning Data ===")
    df_clean = preprocessor.clean_data(df)
    print(f"After cleaning: {list(df_clean.columns)}")
    
    # Feature engineering
    print("\n=== Step 3: Feature Engineering ===")
    df_features = preprocessor.engineer_features(df_clean)
    print(f"After feature engineering: {list(df_features.columns)}")
    print(f"Shape: {df_features.shape}")
    
    # Check which expected features are missing
    missing_features = [f for f in feature_names if f not in df_features.columns]
    extra_features = [f for f in df_features.columns if f not in feature_names]
    
    print(f"\nMissing features: {missing_features}")
    print(f"Extra features: {extra_features}")
    
    # Add missing features
    for feature_name in feature_names:
        if feature_name not in df_features.columns:
            if "_smooth" in feature_name:
                original_name = feature_name.replace("_smooth", "")
                if original_name in df_features.columns:
                    df_features[feature_name] = df_features[original_name]
                else:
                    df_features[feature_name] = 0.0
            elif "_rolling_std" in feature_name:
                df_features[feature_name] = 0.1
            elif "_rolling_mean" in feature_name:
                original_name = feature_name.replace("_rolling_mean", "")
                if original_name in df_features.columns:
                    df_features[feature_name] = df_features[original_name]
                else:
                    df_features[feature_name] = 0.0
            elif feature_name == "temp_diff":
                if "Process temperature [K]" in df_features.columns and "Air temperature [K]" in df_features.columns:
                    df_features[feature_name] = df_features["Process temperature [K]"] - df_features["Air temperature [K]"]
                else:
                    df_features[feature_name] = 10.0
            elif feature_name == "power":
                if "Torque [Nm]" in df_features.columns and "Rotational speed [rpm]" in df_features.columns:
                    df_features[feature_name] = df_features["Torque [Nm]"] * df_features["Rotational speed [rpm]"] / 9550
                else:
                    df_features[feature_name] = 5.0
            elif feature_name == "tool_wear_rate":
                df_features[feature_name] = 0.0
            else:
                df_features[feature_name] = 0.0
    
    print(f"After adding missing features: {list(df_features.columns)}")
    
    # Reorder and select only required features
    df_features = df_features[feature_names]
    print(f"After reordering: {list(df_features.columns)}")
    print(f"Final shape: {df_features.shape}")
    
    # Normalize
    print("\n=== Step 4: Normalization ===")
    df_normalized = preprocessor.normalize_data(df_features, fit=False)
    print(f"After normalization: {list(df_normalized.columns)}")
    print(f"Shape: {df_normalized.shape}")
    
    # Prepare features
    print("\n=== Step 5: Preparing Features ===")
    features, feature_cols = preprocessor.prepare_features(df_normalized)
    print(f"Final features shape: {features.shape}")
    print(f"Feature columns: {feature_cols}")
    
    # Test prediction
    print("\n=== Step 6: Testing Prediction ===")
    try:
        prediction = model.predict(features)
        print(f"Prediction successful: {prediction}")
        
        if hasattr(model, 'decision_function'):
            decision = model.decision_function(features)
            print(f"Decision function: {decision}")
    except Exception as e:
        print(f"Prediction failed: {e}")

if __name__ == "__main__":
    debug_preprocessing()
