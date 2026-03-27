"""
Model training module for Anomaly Detection Engine
Handles training, evaluation, and saving of anomaly detection models
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import logging
from typing import Tuple, Dict, Any
import time

from config import (
    DATA_PATH, MODEL_PATH, SCALER_PATH, ISOLATION_FOREST_CONFIG,
    TRAIN_TEST_SPLIT, FEATURE_COLUMNS, SENSOR_CONFIG
)
from preprocessing import DataPreprocessor
from utils import setup_logging, save_model, calculate_model_metrics

class AnomalyDetectionModel:
    """Main class for training and managing anomaly detection models"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.preprocessor = DataPreprocessor()
        self.model = None
        self.feature_stats = {}
        self.feature_names = []
        
    def load_and_prepare_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Load and prepare data for training"""
        self.logger.info("Loading and preparing training data")
        
        # Preprocess data for training
        features, feature_names = self.preprocessor.preprocess_for_training(DATA_PATH)
        self.feature_names = feature_names
        
        # Load original data to get labels
        df = self.preprocessor.load_data(DATA_PATH)
        df_clean = self.preprocessor.clean_data(df)
        
        # Use 'Target' column as labels (1 = failure, 0 = no failure)
        if 'Target' in df_clean.columns:
            labels = df_clean['Target'].values
        else:
            # If no labels available, create synthetic labels based on statistical outliers
            self.logger.warning("No labels found in dataset, creating synthetic labels")
            labels = self._create_synthetic_labels(df_clean)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, 
            test_size=1-TRAIN_TEST_SPLIT, 
            random_state=42,
            stratify=labels if len(np.unique(labels)) > 1 else None
        )
        
        # Calculate feature statistics on training data
        train_df = pd.DataFrame(X_train, columns=self.feature_names)
        self.feature_stats = self.preprocessor.get_feature_statistics(train_df)
        
        # Store feature names in preprocessor for prediction use
        self.preprocessor.feature_names = self.feature_names
        
        self.logger.info(f"Data prepared - Train: {X_train.shape}, Test: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def _create_synthetic_labels(self, df: pd.DataFrame) -> np.ndarray:
        """Create synthetic anomaly labels based on statistical outliers"""
        labels = np.zeros(len(df))
        
        for col in FEATURE_COLUMNS:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Mark outliers as anomalies
                outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                labels[outlier_mask] = 1
        
        return labels
    
    def train_model(self, X_train: np.ndarray) -> Dict[str, Any]:
        """Train the Isolation Forest model"""
        self.logger.info("Training Isolation Forest model")
        start_time = time.time()
        
        # Initialize model with configuration
        self.model = IsolationForest(**ISOLATION_FOREST_CONFIG)
        
        # Train model
        self.model.fit(X_train)
        
        training_time = time.time() - start_time
        self.logger.info(f"Model training completed in {training_time:.2f} seconds")
        
        return {
            "training_time": training_time,
            "model_config": ISOLATION_FOREST_CONFIG,
            "n_features": X_train.shape[1],
            "n_samples": X_train.shape[0]
        }
    
    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Evaluate model performance on test data"""
        self.logger.info("Evaluating model performance")
        
        # Get predictions
        predictions = self.model.predict(X_test)
        # Convert predictions: 1 = normal, -1 = anomaly -> 0 = normal, 1 = anomaly
        predictions_binary = (predictions == -1).astype(int)
        
        # Calculate metrics
        metrics = calculate_model_metrics(y_test, predictions_binary)
        
        # Add confusion matrix
        cm = confusion_matrix(y_test, predictions_binary)
        
        # Calculate detection rate
        anomaly_mask = y_test == 1
        if np.sum(anomaly_mask) > 0:
            anomaly_detection_rate = np.sum(predictions_binary[anomaly_mask] == 1) / np.sum(anomaly_mask)
        else:
            anomaly_detection_rate = 0.0
        
        evaluation_results = {
            "metrics": metrics,
            "confusion_matrix": cm.tolist(),
            "anomaly_detection_rate": anomaly_detection_rate,
            "test_samples": len(y_test),
            "predicted_anomalies": np.sum(predictions_binary),
            "actual_anomalies": np.sum(y_test)
        }
        
        self.logger.info(f"Model evaluation completed: {evaluation_results}")
        return evaluation_results
    
    def save_trained_model(self) -> bool:
        """Save the trained model and preprocessing components"""
        if self.model is None:
            self.logger.error("No trained model to save")
            return False
        
        # Save model and scaler
        success = save_model(
            self.model, 
            self.preprocessor.scaler, 
            MODEL_PATH, 
            SCALER_PATH
        )
        
        if success:
            # Save feature statistics
            import json
            stats_path = MODEL_PATH.parent / "feature_stats.json"
            with open(stats_path, 'w') as f:
                json.dump(self.feature_stats, f, indent=2)
            
            # Save feature names
            names_path = MODEL_PATH.parent / "feature_names.json"
            with open(names_path, 'w') as f:
                json.dump(self.feature_names, f, indent=2)
        
        return success
    
    def train_and_evaluate(self) -> Dict[str, Any]:
        """Complete training and evaluation pipeline"""
        self.logger.info("Starting complete training pipeline")
        
        try:
            # Load and prepare data
            X_train, X_test, y_train, y_test = self.load_and_prepare_data()
            
            # Train model
            training_info = self.train_model(X_train)
            
            # Evaluate model
            evaluation_results = self.evaluate_model(X_test, y_test)
            
            # Save model
            save_success = self.save_trained_model()
            
            results = {
                "training": training_info,
                "evaluation": evaluation_results,
                "model_saved": save_success,
                "feature_stats": self.feature_stats,
                "feature_names": self.feature_names
            }
            
            self.logger.info("Training pipeline completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in training pipeline: {e}")
            raise
    
    def load_existing_model(self) -> bool:
        """Load existing trained model"""
        try:
            import json
            from utils import load_model
            
            self.model, self.preprocessor.scaler = load_model(MODEL_PATH, SCALER_PATH)
            
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
                    # Store feature names in preprocessor for prediction use
                    self.preprocessor.feature_names = self.feature_names
            
            self.logger.info("Existing model loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading existing model: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the trained model"""
        if self.model is None:
            return {"status": "No model trained"}
        
        info = {
            "model_type": "Isolation Forest",
            "model_config": ISOLATION_FOREST_CONFIG,
            "n_features": len(self.feature_names),
            "feature_names": self.feature_names,
            "feature_stats": self.feature_stats,
            "model_path": str(MODEL_PATH),
            "scaler_path": str(SCALER_PATH)
        }
        
        return info

def main():
    """Main function to train the anomaly detection model"""
    logger = setup_logging()
    
    try:
        # Initialize model trainer
        trainer = AnomalyDetectionModel()
        
        # Train and evaluate
        results = trainer.train_and_evaluate()
        
        # Print results
        logger.info("Training Results:")
        logger.info(f"Training time: {results['training']['training_time']:.2f} seconds")
        logger.info(f"Model saved: {results['model_saved']}")
        
        logger.info("Evaluation Results:")
        metrics = results['evaluation']['metrics']
        for metric, value in metrics.items():
            logger.info(f"{metric}: {value:.3f}")
        
        logger.info(f"Anomaly detection rate: {results['evaluation']['anomaly_detection_rate']:.3f}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in main training function: {e}")
        raise

if __name__ == "__main__":
    main()
