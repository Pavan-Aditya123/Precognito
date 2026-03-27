"""
Simple test to check scaler feature names
"""

import json
import pickle
from config import MODEL_PATH, SCALER_PATH

# Load scaler
with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

print(f"Scaler feature names: {scaler.feature_names_in_}")
print(f"Number of features: {len(scaler.feature_names_in_)}")

# Load expected feature names
with open(MODEL_PATH.parent / "feature_names.json", 'r') as f:
    feature_names = json.load(f)

print(f"Expected feature names: {feature_names}")
print(f"Number of expected features: {len(feature_names)}")

# Check differences
scaler_features = set(scaler.feature_names_in_)
expected_features = set(feature_names)

missing_from_scaler = expected_features - scaler_features
extra_in_scaler = scaler_features - expected_features

print(f"Missing from scaler: {missing_from_scaler}")
print(f"Extra in scaler: {extra_in_scaler}")
