"""
MQTT Worker module for ingesting telemetry data from an MQTT broker.
"""
import json
import logging
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from precognito.ingestion.core import process_ingestion

load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = "telemetry/#"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback triggered when the client connects to the MQTT broker.

    Args:
        client (paho.mqtt.client.Client): The client instance for this callback.
        userdata: The private user data as set in Client() or user_data_set().
        flags (dict): Response flags sent by the broker.
        rc (int): The connection result.
        properties (paho.mqtt.packettypes.Properties, optional): MQTT v5.0 properties.
    """
    if rc == 0:
        logger.info(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        logger.info(f"Subscribed to {MQTT_TOPIC}")
    else:
        logger.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback triggered when a message is received from the MQTT broker.

    Args:
        client (paho.mqtt.client.Client): The client instance for this callback.
        userdata: The private user data as set in Client() or user_data_set().
        msg (paho.mqtt.client.MQTTMessage): An instance of MQTTMessage.
    """
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        
        # Expecting telemetry/device_id or device_id in payload
        device_id = payload.get("device_id")
        if not device_id and "/" in topic:
            device_id = topic.split("/")[-1]
            
        if device_id:
            logger.info(f"Received MQTT telemetry for {device_id}")
            result = process_ingestion(device_id, payload)
            if result and result.get("anomaly_analysis", {}).get("anomaly_detected"):
                logger.warning(f"⚠️ ANOMALY DETECTED for {device_id}: {result['anomaly_analysis']['reason']}")
        else:
            logger.warning(f"Received MQTT message without device_id on topic {topic}")
            
    except json.JSONDecodeError:
        logger.error(f"Failed to decode MQTT payload: {msg.payload}")
    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}")

def run_worker():
    """Initializes and runs the MQTT client to listen for incoming telemetry.
    """
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        logger.error(f"MQTT Worker error: {e}")

if __name__ == "__main__":
    run_worker()
