"""
Module for tracking device heartbeats and status.
"""
from datetime import datetime

device_status = {}

def update_heartbeat(device_id):
    """Updates the last seen timestamp for a device.

    Args:
        device_id (str): The unique identifier of the device.
    """
    device_status[device_id] = datetime.now()

def check_device_status(device_id):
    """Checks the operational status of a device based on its heartbeat.

    Args:
        device_id (str): The unique identifier of the device.

    Returns:
        str: The status of the device ("Active", "Sensor Not Transmitting", or "No Data").
    """
    last_seen = device_status.get(device_id)

    if not last_seen:
        return "No Data"

    diff = (datetime.now() - last_seen).seconds

    if diff > 5:
        return "Sensor Not Transmitting"
    return "Active"
