"""
Debug script to see what columns are being created
"""

import json
import pandas as pd
import numpy as np
from preprocessing import DataPreprocessor
from utils import load_model
from config import MODEL_PATH, SCALER_PATH

def debug_columns():
    """Debug what columns are created during prediction"""
    print("=== Debugging Column Creation ===")
    
    # Load model and scaler
    model, scaler = load_model(MODEL_PATH, SCALER_PATH)
    
    # Load feature names
    with open(MODEL_PATH.parent / "feature_names.json", 'r') as f:
        feature_names = json.load(f)
    
    print(f"Expected feature names ({len(feature_names)}):")
    for i, name in enumerate(feature_names):
        print(f"  {i}: {name}")
    
    print(f"\nScaler feature names ({len(scaler.feature_names_in_)}):")
    for i, name in enumerate(scaler.feature_names_in_):
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
    
    # Step by step
    df = pd.DataFrame([test_data])
    print(f"\nInitial DataFrame columns: {list(df.columns)}")
    
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
    
    print(f"After mapping: {list(df.columns)}")
    
    # Add defaults
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
    
    print(f"After defaults: {list(df.columns)}")
    
    # Clean data
    df_clean = preprocessor.clean_data(df)
    print(f"After cleaning: {list(df_clean.columns)}")
    
    # Feature engineering
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
    
    # Select only expected features
    df_selected = df_features[feature_names]
    print(f"After selecting expected features: {list(df_selected.columns)}")
    print(f"Final shape: {df_selected.shape}")

if __name__ == "__main__":
    debug_columns()
