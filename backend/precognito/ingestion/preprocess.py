"""
Module for preprocessing and standardizing incoming sensor data.
"""
import logging

logger = logging.getLogger(__name__)

def preprocess(data: dict) -> dict:
    """Standardize and clean incoming sensor data.

    Args:
        data (dict): Raw input data from sensors with varying keys and formats.

    Returns:
        dict: Standardized dictionary containing key sensor metrics (temperature, 
              vibration, pressure, torque, tool_wear, vibration_rms, 
              freq_spike_1x, freq_spike_bpfo).
    """
    processed = {}
    
    # Required fields mapping
    mapping = {
        "temperature": ["temperature", "temp", "temp_c", "Air temperature [K]"],
        "vibration": ["vibration", "vib", "rotational_speed", "Rotational speed [rpm]"],
        "pressure": ["pressure", "press", "psi"],
        "torque": ["torque", "Torque [Nm]"],
        "tool_wear": ["tool_wear", "Tool wear [min]"],
        # Predictive features
        "vibration_rms": ["vibration_rms", "rms_vibration", "vibration"],
        "freq_spike_1x": ["freq_spike_1x", "1x_spike"],
        "freq_spike_bpfo": ["freq_spike_bpfo", "bpfo_spike"]
    }

    for key, aliases in mapping.items():
        val = None
        for alias in aliases:
            if alias in data:
                val = data[alias]
                break
        
        if val is not None:
            try:
                processed[key] = round(float(val), 2)
            except (ValueError, TypeError):
                logger.warning(f"Failed to convert {key} value: {val}")
                processed[key] = 0.0
        else:
            # Default values if not present
            processed[key] = 0.0

    return processed
