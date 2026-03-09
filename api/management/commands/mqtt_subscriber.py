import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.conf import settings
import logging
import json
from api.models import RFIDScan  # Replace with your actual model import
from django.utils import timezone

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Connects to EMQX as an MQTT subscriber and listens on /transaction'

    def add_arguments(self, parser):
        parser.add_argument(
            '--broker',
            type=str,
            default=getattr(settings, 'MQTT_BROKER', 'u81317a2.ala.eu-central-1.emqxsl.com'),
            help='MQTT broker host'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=getattr(settings, 'MQTT_PORT', 8883),
            help='MQTT broker port'
        )
        parser.add_argument(
            '--username',
            type=str,
            default=getattr(settings, 'MQTT_USERNAME', 'django_subscriber'),
            help='MQTT username'
        )
        parser.add_argument(
            '--password',
            type=str,
            default=getattr(settings, 'MQTT_PASSWORD', ''),
            help='MQTT password'
        )
        parser.add_argument(
            '--topic',
            type=str,
            default=getattr(settings, 'MQTT_TOPIC', '/transaction'),
            help='Topic to subscribe to'
        )

    def handle(self, *args, **options):
        broker = options['broker']
        port = options['port']
        username = options['username']
        password = options['password']
        topic = options['topic']

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.info("✅ Connected to MQTT broker")
                client.subscribe(topic)
                logger.info(f"Subscribed to {topic}")
            else:
                logger.error(f"Connection failed with code {rc}")

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()
                logger.info(f"Received: {payload} on {msg.topic}")

                # Save to database – adjust to your model
                # Example for RFIDScan:
                RFIDScan.objects.create(
                    rfid_tag=payload,
                    rfid=None,  # You can try to link if needed
                    payload={"topic": msg.topic, "payload": payload, "qos": msg.qos},
                    created_at=timezone.now()
                )
                logger.debug("Saved to database")
            except Exception as e:
                logger.error(f"Error processing message: {e}")

        # Create MQTT client
        client = mqtt.Client()
        client.username_pw_set(username, password)
        client.tls_set()  # Uses system CA certs (required for EMQX Serverless)

        client.on_connect = on_connect
        client.on_message = on_message

        try:
            logger.info(f"Connecting to {broker}:{port} as {username}...")
            client.connect(broker, port, 60)
            client.loop_forever()
        except KeyboardInterrupt:
            logger.info("Stopping subscriber...")
            client.disconnect()
        except Exception as e:
            logger.error(f"Fatal error: {e}")