from pydantic import BaseModel

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

class PredictionResponse(BaseModel):
    """Schema for machine health prediction responses.

    Attributes:
        rul_hours: Estimated Remaining Useful Life in hours.
        confidence_pct: Confidence score of the prediction as a percentage.
        fault_type: Predicted type of fault.
        risk_level: Assigned risk level (e.g., Normal, Warning, High-Risk).
        recommendation: Recommended maintenance action.
    """
    rul_hours: float
    confidence_pct: float
    fault_type: str
    risk_level: str
    recommendation: str
