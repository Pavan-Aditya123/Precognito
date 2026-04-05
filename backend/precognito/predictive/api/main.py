from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os

# Add parent directory to path so it can import ml module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml.inference_engine import PredictiveInferenceEngine

app = FastAPI(title="Precognito - Predictive Inference Engine API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inference_engine = None
latest_prediction = {
    "rul_hours": 500.0,
    "confidence_pct": 100,
    "fault_type": "Normal",
    "risk_level": "Healthy",
    "recommendation": "Normal Operation"
}

class TelemetryPayload(BaseModel):
    """Schema for machine telemetry data.

    Attributes:
        machine_id: Unique identifier for the machine.
        vibration_rms: Root Mean Square vibration value.
        temperature: Operating temperature of the machine.
        freq_spike_1x: Frequency spike at 1x rotational speed.
        freq_spike_bpfo: Frequency spike at Ball Pass Frequency Outer race.
    """
    machine_id: int
    vibration_rms: float
    temperature: float
    freq_spike_1x: float
    freq_spike_bpfo: float

@app.on_event("startup")
def load_models():
    """Load machine learning models during application startup.

    If the model files exist, it initializes the PredictiveInferenceEngine.
    Otherwise, it prints a warning message.
    """
    global inference_engine
    if os.path.exists("models/rul_model.joblib"):
        inference_engine = PredictiveInferenceEngine(model_dir="models")
    else:
        print("Warning: Models not trained yet. Run python -m ml.train first.")

@app.post("/predict/rul")
def predict_rul(data: TelemetryPayload):
    """Predict Remaining Useful Life (RUL) for a machine based on telemetry data.

    Args:
        data: A TelemetryPayload object containing machine telemetry values.

    Returns:
        A dictionary containing the status, machine_id, and the prediction results.

    Raises:
        HTTPException: If the inference engine models are not loaded.
    """
    global inference_engine
    if not inference_engine:
        if os.path.exists("models/rul_model.joblib"):
            inference_engine = PredictiveInferenceEngine(model_dir="models")
        else:
            raise HTTPException(status_code=503, detail="Models not loaded. Train models first.")
    
    telemetry_data = {
        "vibration_rms": data.vibration_rms,
        "temperature": data.temperature,
        "freq_spike_1x": data.freq_spike_1x,
        "freq_spike_bpfo": data.freq_spike_bpfo
    }
    
    
    result = inference_engine.predict(telemetry_data)
    
    global latest_prediction
    latest_prediction = {
        "rul_hours": result.get("predicted_rul_hours"),
        "confidence_pct": result.get("confidence_score_percent"),
        "fault_type": result.get("predicted_fault_type"),
        "risk_level": result.get("risk_level"),
        "recommendation": result.get("recommendation")
    }
    
    return {
        "status": "success",
        "machine_id": data.machine_id,
        "prediction": result
    }

@app.get("/api/predict")
def get_predict():
    """Retrieve the latest prediction result.

    Returns:
        A dictionary containing the latest prediction data.
    """
    return latest_prediction

# Mount frontend directory for static serving
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
os.makedirs(frontend_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the frontend index.html file.

    Returns:
        A FileResponse if index.html exists, otherwise a message dictionary.
    """
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend not found. Please create frontend folder with index.html"}
