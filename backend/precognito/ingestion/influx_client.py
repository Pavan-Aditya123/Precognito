"""
InfluxDB client module for saving and querying sensor telemetry and analysis results.
"""
import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

# InfluxDB Configuration
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "precognito_super_secret_token_123")
INFLUX_ORG = os.getenv("INFLUX_ORG", "precognito_org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "precognito_bucket")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def save_sensor_data(device_id: str, data: dict):
    """Saves raw sensor data to InfluxDB.

    Args:
        device_id (str): The unique identifier of the device.
        data (dict): A dictionary of sensor readings to save.
    """
    point = Point("machine_telemetry") \
        .tag("device_id", device_id) \
        .time(datetime.utcnow(), WritePrecision.NS)

    for key, value in data.items():
        if isinstance(value, (int, float)):
            point.field(key, float(value))
        elif isinstance(value, str):
            point.field(key, value)

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)

def save_anomaly_result(device_id: str, result: dict):
    """Saves anomaly detection results to InfluxDB.

    Args:
        device_id (str): The unique identifier of the device.
        result (dict): A dictionary containing anomaly detection results 
                       (severity, anomaly_detected, confidence, reason).
    """
    point = Point("anomaly_results") \
        .tag("device_id", device_id) \
        .tag("severity", result.get("severity", "LOW")) \
        .field("anomaly_detected", bool(result.get("anomaly_detected", False))) \
        .field("confidence", float(result.get("confidence", 0.0))) \
        .field("reason", str(result.get("reason", ""))) \
        .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)

def save_predictive_result(device_id: str, result: dict):
    """Saves Remaining Useful Life (RUL) and fault prediction results to InfluxDB.

    Args:
        device_id (str): The unique identifier of the device.
        result (dict): A dictionary containing predictive results 
                       (risk_level, predicted_fault_type, predicted_rul_hours, 
                       confidence_score_percent).
    """
    point = Point("predictive_results") \
        .tag("device_id", device_id) \
        .tag("risk_level", result.get("risk_level", "Normal")) \
        .tag("predicted_fault_type", result.get("predicted_fault_type", "None")) \
        .field("predicted_rul_hours", float(result.get("predicted_rul_hours", 0.0))) \
        .field("confidence_score_percent", float(result.get("confidence_score_percent", 0.0))) \
        .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)

def query_latest_data(device_id: str, measurement: str = "machine_telemetry"):
    """Queries the latest data for a specific device and measurement.

    Args:
        device_id (str): The unique identifier of the device.
        measurement (str, optional): The InfluxDB measurement name. Defaults to "machine_telemetry".

    Returns:
        list: A list of FluxTable objects containing the query results.
    """
    query = f'from(bucket: "{INFLUX_BUCKET}") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "{measurement}") |> filter(fn: (r) => r["device_id"] == "{device_id}") |> last()'
    return query_api.query(query, org=INFLUX_ORG)

def query_historical_data(device_id: str, measurement: str, range_start: str = "-24h"):
    """Queries historical data for a device over a specific time range.

    Args:
        device_id (str): The unique identifier of the device.
        measurement (str): The InfluxDB measurement name.
        range_start (str, optional): The start of the time range (e.g., "-24h"). Defaults to "-24h".

    Returns:
        list: A list of FluxTable objects containing the query results.
    """
    query = f'from(bucket: "{INFLUX_BUCKET}") |> range(start: {range_start}) |> filter(fn: (r) => r["_measurement"] == "{measurement}") |> filter(fn: (r) => r["device_id"] == "{device_id}") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
    return query_api.query(query, org=INFLUX_ORG)

def get_all_devices(measurement: str = "machine_telemetry"):
    """Retrieves a list of all unique device IDs that have sent data.

    Args:
        measurement (str, optional): The InfluxDB measurement name to scan. Defaults to "machine_telemetry".

    Returns:
        list: A list of unique device ID strings.
    """
    query = f'from(bucket: "{INFLUX_BUCKET}") |> range(start: -30d) |> filter(fn: (r) => r["_measurement"] == "{measurement}") |> keep(columns: ["device_id"]) |> unique(column: "device_id")'
    tables = query_api.query(query, org=INFLUX_ORG)
    devices = []
    for table in tables:
        for record in table.records:
            devices.append(record.values.get("device_id"))
    return list(set(devices))

def check_sustained_thermal(device_id: str, threshold: float = 70.0, window: str = "5m"):
    """Checks if temperature has been sustained above a threshold over a time window.

    Args:
        device_id (str): The unique identifier of the device.
        threshold (float, optional): The temperature threshold. Defaults to 70.0.
        window (str, optional): The time window to check (e.g., "5m"). Defaults to "5m".

    Returns:
        bool: True if all readings in the window are above the threshold, False otherwise.
    """
    query = f'from(bucket: "{INFLUX_BUCKET}") |> range(start: -{window}) |> filter(fn: (r) => r["_measurement"] == "machine_telemetry") |> filter(fn: (r) => r["device_id"] == "{device_id}") |> filter(fn: (r) => r["_field"] == "temperature")'
    tables = query_api.query(query, org=INFLUX_ORG)
    
    values = []
    for table in tables:
        for record in table.records:
            values.append(record.get_value())
            
    if not values:
        return False
        
    return all(v > threshold for v in values)
