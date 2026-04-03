"""
Notification module for sending alerts via external services like NTFY.sh.
"""
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Use a unique topic name for the project
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "precognito_alerts_demo")
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

def send_external_notification(title: str, message: str, priority: str = "default", tags: list = None):
    """Sends a notification via NTFY.sh.

    Args:
        title (str): The title of the notification.
        message (str): The body text of the notification.
        priority (str, optional): Priority level (min, low, default, high, urgent). 
                                  Defaults to "default".
        tags (list, optional): A list of emoji tags or keywords for the notification.
    """
    headers = {
        "Title": title,
        "Priority": priority,
    }
    
    if tags:
        headers["Tags"] = ",".join(tags)
        
    try:
        response = requests.post(NTFY_URL, data=message, headers=headers, timeout=5)
        if response.status_code == 200:
            logger.info(f"External notification sent successfully to topic: {NTFY_TOPIC}")
        else:
            logger.error(f"Failed to send NTFY notification: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Error sending external notification: {e}")

def notify_critical_anomaly(device_id: str, reason: str):
    """Sends a critical anomaly notification.

    Args:
        device_id (str): The ID of the affected device.
        reason (str): The reason for the anomaly.
    """
    send_external_notification(
        title=f"🚨 CRITICAL ANOMALY: {device_id}",
        message=f"Machine failure imminent! Reason: {reason}. Check dashboard immediately.",
        priority="urgent",
        tags=["warning", "skull", "factory"]
    )

def notify_safety_alert(device_id: str, temp: float):
    """Sends a safety breach notification for sustained high temperatures.

    Args:
        device_id (str): The ID of the affected device.
        temp (float): The detected temperature.
    """
    send_external_notification(
        title=f"🔥 SAFETY BREACH: {device_id}",
        message=f"Sustained high temperature detected: {temp}°C. Fire risk high!",
        priority="urgent",
        tags=["fire", "ambulance", "warning"]
    )
