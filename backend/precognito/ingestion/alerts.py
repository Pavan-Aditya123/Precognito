"""
Module for simple threshold-based alerting.
"""
def check_alerts(data):
    """Checks sensor data against predefined thresholds to determine alert status.

    Args:
        data (dict): A dictionary containing sensor telemetry data, specifically 'vibration'.

    Returns:
        str: The alert level ("CRITICAL", "WARNING", or "NORMAL").
    """
    # Standard thresholds matching SENSOR_CONFIG in anomaly/core.py
    # vibration: min: 1000.0, max: 2000.0, critical: 2500.0
    vibration = data.get("vibration", 0)
    
    if vibration > 2500:
        return "CRITICAL"
    elif vibration > 2000:
        return "WARNING"
    return "NORMAL"
