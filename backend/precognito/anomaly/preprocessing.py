"""
Data preprocessing module for Anomaly Detection Engine
Handles cleaning, filtering, normalization, and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
import logging
from typing import Dict, List, Tuple, Optional
from config import PREPROCESSING_CONFIG, FEATURE_COLUMNS, SENSOR_CONFIG

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handles all data preprocessing operations for anomaly detection"""
    
    def __init__(self):
        self.scaler = None
        self.imputer = None
        self.feature_stats = {}
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load dataset from CSV file"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded dataset with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean raw data by handling missing values and outliers"""
        df_clean = df.copy()
        
        # Handle missing values
        if df_clean.isnull().sum().sum() > 0:
            logger.info("Handling missing values")
            method = PREPROCESSING_CONFIG["fill_missing_method"]
            
            if method == "forward_fill":
                df_clean = df_clean.fillna(method='ffill').fillna(method='bfill')
            elif method == "mean":
                df_clean = df_clean.fillna(df_clean.mean())
            elif method == "median":
                df_clean = df_clean.fillna(df_clean.median())
        
        # Remove obvious outliers using IQR method
        for col in FEATURE_COLUMNS:
            if col in df_clean.columns:
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Cap outliers instead of removing them
                df_clean[col] = df_clean[col].clip(lower_bound, upper_bound)
        
        logger.info(f"Data cleaning completed. Shape: {df_clean.shape}")
        return df_clean
    
    def apply_smoothing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply smoothing to reduce noise in time-series data"""
        df_smooth = df.copy()
        window_size = PREPROCESSING_CONFIG["rolling_window_size"]
        method = PREPROCESSING_CONFIG["smoothing_method"]
        
        for col in FEATURE_COLUMNS:
            if col in df_smooth.columns:
                if method == "rolling_mean":
                    df_smooth[f"{col}_smooth"] = df_smooth[col].rolling(
                        window=window_size, min_periods=1
                    ).mean()
                elif method == "rolling_median":
                    df_smooth[f"{col}_smooth"] = df_smooth[col].rolling(
                        window=window_size, min_periods=1
                    ).median()
        
        logger.info(f"Smoothing applied using {method} with window size {window_size}")
        return df_smooth
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create additional features for better anomaly detection"""
        df_features = df.copy()
        
        # Temperature difference
        if "Air temperature [K]" in df_features.columns and "Process temperature [K]" in df_features.columns:
            df_features["temp_diff"] = df_features["Process temperature [K]"] - df_features["Air temperature [K]"]
        
        # Power calculation (Torque * Rotational speed)
        if "Torque [Nm]" in df_features.columns and "Rotational speed [rpm]" in df_features.columns:
            df_features["power"] = df_features["Torque [Nm]"] * df_features["Rotational speed [rpm]"] / 9550  # Convert to kW
        
        # Tool wear rate
        if "Tool wear [min]" in df_features.columns:
            df_features["tool_wear_rate"] = df_features["Tool wear [min]"].diff().fillna(0)
        
        # Rolling statistics for each feature
        window_size = PREPROCESSING_CONFIG["rolling_window_size"]
        for col in FEATURE_COLUMNS:
            if col in df_features.columns:
                df_features[f"{col}_rolling_std"] = df_features[col].rolling(
                    window=window_size, min_periods=1
                ).std().fillna(0)
                
                df_features[f"{col}_rolling_mean"] = df_features[col].rolling(
                    window=window_size, min_periods=1
                ).mean()
        
        logger.info("Feature engineering completed")
        return df_features
    
    def normalize_data(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Normalize/scale the data"""
        df_norm = df.copy()
        
        if fit:
            # During training: scale all numeric columns except excluded ones
            exclude_cols = ['UDI', 'Target', 'Failure Type', 'Product ID', 'Type']
            numeric_columns = [col for col in df_norm.select_dtypes(include=[np.number]).columns 
                            if col not in exclude_cols]
            
            scaling_method = PREPROCESSING_CONFIG["scaling_method"]
            
            if scaling_method == "standard":
                self.scaler = StandardScaler()
            elif scaling_method == "minmax":
                self.scaler = MinMaxScaler()
            
            df_norm[numeric_columns] = self.scaler.fit_transform(df_norm[numeric_columns])
            logger.info(f"Data fitted and transformed using {scaling_method} scaling on {len(numeric_columns)} columns")
        else:
            # During prediction: only use the columns the scaler was trained on
            if self.scaler is None:
                raise ValueError("Scaler not fitted. Call with fit=True first.")
            
            # Use only the columns that the scaler expects
            numeric_columns = list(self.scaler.feature_names_in_)
            
            # Ensure all required columns exist
            for col in numeric_columns:
                if col not in df_norm.columns:
                    df_norm[col] = 0.0
            
            df_norm[numeric_columns] = self.scaler.transform(df_norm[numeric_columns])
            logger.info(f"Data transformed using existing scaler on {len(numeric_columns)} columns")
            
            # After scaling, only return the scaler columns
            df_norm = df_norm[numeric_columns]
        
        return df_norm
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract and prepare features for model training/prediction"""
        # If we have stored feature names and they exist in dataframe, use them
        if hasattr(self, 'feature_names') and self.feature_names:
            # Only use the stored feature names that exist in the dataframe
            available_features = [feature_name for feature_name in self.feature_names if feature_name in df.columns]
            
            if available_features:
                features = df[available_features].values
                logger.info(f"Prepared features with shape: {features.shape}")
                return features, available_features
        
        # Fallback: Get all numeric columns that could be features
        feature_cols = []
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                feature_cols.append(col)
        
        # Remove non-feature columns
        exclude_cols = ['UDI', 'Target', 'Failure Type', 'Product ID', 'Type']
        feature_cols = [col for col in feature_cols if col not in exclude_cols]
        
        features = df[feature_cols].values
        logger.info(f"Prepared features with shape: {features.shape}")
        
        return features, feature_cols
    
    def preprocess_for_training(self, file_path: str) -> Tuple[np.ndarray, List[str]]:
        """Complete preprocessing pipeline for training data"""
        logger.info("Starting preprocessing pipeline for training")
        
        # Load and clean data
        df = self.load_data(file_path)
        df_clean = self.clean_data(df)
        
        # Apply smoothing and feature engineering
        df_smooth = self.apply_smoothing(df_clean)
        df_features = self.engineer_features(df_smooth)
        
        # Store all feature names first
        all_numeric_cols = df_features.select_dtypes(include=[np.number]).columns.tolist()
        exclude_cols = ['UDI', 'Target', 'Failure Type', 'Product ID', 'Type']
        potential_features = [col for col in all_numeric_cols if col not in exclude_cols]
        
        # Normalize data on all potential features
        df_normalized = self.normalize_data(df_features, fit=True)
        
        # Prepare features - this will filter to the actual features we want
        features, feature_names = self.prepare_features(df_normalized)
        
        # Store the final feature names for later use
        self.feature_names = feature_names
        
        logger.info("Training data preprocessing completed")
        return features, feature_names
    
    def preprocess_for_prediction(self, data: Dict) -> np.ndarray:
        """Preprocess single data point for real-time prediction"""
        # Convert dict to DataFrame with all required columns
        df = pd.DataFrame([data])
        
        # Map input keys to actual column names and add missing columns
        column_mapping = {
            "temperature": "Process temperature [K]",
            "vibration": "Rotational speed [rpm]",
            "torque": "Torque [Nm]",
            "tool_wear": "Tool wear [min]",
            "air_temperature": "Air temperature [K]"
        }
        
        # Add mapped columns
        for key, col_name in column_mapping.items():
            if key in data and col_name not in df.columns:
                df[col_name] = data[key]
        
        # Add missing columns with default values to match training features
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
        
        # Apply same preprocessing steps
        df_clean = self.clean_data(df)
        df_features = self.engineer_features(df_clean)
        
        # Ensure all required features are present with correct names
        if hasattr(self, 'feature_names') and self.feature_names:
            # Add missing features with default values
            for feature_name in self.feature_names:
                if feature_name not in df_features.columns:
                    if "_smooth" in feature_name:
                        # Use original value for smooth features
                        original_name = feature_name.replace("_smooth", "")
                        if original_name in df_features.columns:
                            df_features[feature_name] = df_features[original_name]
                        else:
                            df_features[feature_name] = 0.0
                    elif "_rolling_std" in feature_name:
                        df_features[feature_name] = 0.1  # Small default std
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
            
            # Select only the required features before normalization
            df_features = df_features[self.feature_names]
        
        df_normalized = self.normalize_data(df_features, fit=False)
        
        features, _ = self.prepare_features(df_normalized)
        return features
    
    def get_feature_statistics(self, df: pd.DataFrame) -> Dict:
        """Calculate and store feature statistics for anomaly scoring"""
        stats = {}
        for col in FEATURE_COLUMNS:
            if col in df.columns:
                stats[col] = {
                    "mean": df[col].mean(),
                    "std": df[col].std(),
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "q25": df[col].quantile(0.25),
                    "q75": df[col].quantile(0.75)
                }
        
        self.feature_stats = stats
        logger.info("Feature statistics calculated")
        return stats
