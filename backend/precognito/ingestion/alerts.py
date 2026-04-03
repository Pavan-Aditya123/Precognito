def check_alerts(data):
    # Standard thresholds matching SENSOR_CONFIG in anomaly/core.py
    # vibration: min: 1000.0, max: 2000.0, critical: 2500.0
    vibration = data.get("vibration", 0)
    
    if vibration > 2500:
        return "CRITICAL"
    elif vibration > 2000:
        return "WARNING"
    return "NORMAL"
