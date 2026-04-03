import logging
from precognito.ingestion.preprocess import preprocess
from precognito.ingestion.heartbeat import update_heartbeat, check_device_status
from precognito.ingestion.alerts import check_alerts
from precognito.ingestion.influx_client import save_sensor_data, save_anomaly_result, save_predictive_result
from precognito.anomaly.core import detect_anomaly
from precognito.predictive.predictive_engine import predict_rul

logger = logging.getLogger(__name__)

def process_ingestion(device_id: str, raw_data: dict):
    """
    Core logic for processing incoming sensor data from any source (HTTP, MQTT, etc.)
    """
    if not device_id:
        logger.error("device_id is required for ingestion")
        return None

    # 1. Preprocess
    processed = preprocess(raw_data)
    
    # 2. Update status/heartbeat
    update_heartbeat(device_id)
    status = check_device_status(device_id)

    # 3. Detect Anomaly
    anomaly_input = {**processed, "machine_id": device_id}
    anomaly_result = detect_anomaly(anomaly_input)

    # 4. Predict RUL
    # Predictive engine uses specific features mapped in preprocess
    predictive_result = predict_rul(processed)

    # 5. Save to InfluxDB
    try:
        save_sensor_data(device_id, processed)
        save_anomaly_result(device_id, anomaly_result)
        save_predictive_result(device_id, predictive_result)
    except Exception as e:
        logger.error(f"Failed to save to InfluxDB: {e}")

    # 6. Check traditional alerts
    alert = check_alerts(processed)

    return {
        "device_id": device_id,
        "processed_data": processed,
        "device_status": status,
        "anomaly_analysis": anomaly_result,
        "predictive_analysis": predictive_result,
        "alert": alert
    }
