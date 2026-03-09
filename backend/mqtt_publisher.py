import paho.mqtt.client as mqtt
import time
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ========== EMQX CONFIGURATION ==========
BROKER = "u81317a2.ala.eu-central-1.emqxsl.com"
PORT = 8883                     # TLS port
USERNAME = "python_publisher"    
PASSWORD = "pythonpublisher"  
TOPIC = "/transaction"
CLIENT_ID = f"publisher-{random.randint(1000, 9999)}"
# =========================================

def on_connect(client, userdata, flags, rc):
    """Callback when the client connects to the broker."""
    if rc == 0:
        logger.info("✅ Connected to EMQX Serverless")
    else:
        logger.error(f"❌ Connection failed with code {rc}")
        # rc meanings:
        # 1: incorrect protocol version
        # 2: invalid client ID
        # 3: server unavailable
        # 4: bad username/password
        # 5: not authorised

def on_publish(client, userdata, mid):
    """Callback when a message is published."""
    logger.debug(f"Message published (mid: {mid})")

def on_disconnect(client, userdata, rc):
    """Callback when disconnected."""
    if rc != 0:
        logger.warning("Unexpected disconnection. Will auto-reconnect.")

# Create client instance
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(USERNAME, PASSWORD)

# Enable TLS (uses system default CA certificates)
client.tls_set()

# Set callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Connect to broker
try:
    logger.info(f"Connecting to {BROKER}:{PORT} as {USERNAME}...")
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()  # start network loop in background
    time.sleep(1)        # give time for connection to establish
except Exception as e:
    logger.error(f"Connection error: {e}")
    exit(1)

# Publish messages periodically
counter = 0
try:
    while True:
        # Generate a sample RFID tag (you can replace this with real data)
        rfid_tag = f"TAG-{counter:05d}"

        # Publish with QoS 1 (at-least-once delivery)
        result = client.publish(TOPIC, rfid_tag, qos=1)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"📤 Published: {rfid_tag} to {TOPIC}")
        else:
            logger.error(f"Failed to publish: {result}")

        counter += 1
        time.sleep(5)   # wait 5 seconds before next message

except KeyboardInterrupt:
    logger.info("Stopping publisher...")
finally:
    client.loop_stop()
    client.disconnect()
    logger.info("Disconnected")