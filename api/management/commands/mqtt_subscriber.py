import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from api.models import RFIDScan  
import json

class Command(BaseCommand):
    help = 'Connects to EMQX as an MQTT subscriber and listens on /transaction'

    def add_arguments(self, parser):
        parser.add_argument('--broker', type=str, default=getattr(settings, 'MQTT_BROKER', 'u81317a2.ala.eu-central-1.emqxsl.com'))
        parser.add_argument('--port', type=int, default=getattr(settings, 'MQTT_PORT', 8883))
        parser.add_argument('--username', type=str, default=getattr(settings, 'MQTT_USERNAME', 'django_subscriber'))
        parser.add_argument('--password', type=str, default=getattr(settings, 'MQTT_PASSWORD', ''))
        parser.add_argument('--topic', type=str, default=getattr(settings, 'MQTT_TOPIC', '/transaction'))

    def handle(self, *args, **options):
        broker = options['broker']
        port = options['port']
        username = options['username']
        password = options['password']
        topic = options['topic']

        self.stdout.write(f"🔌 Connecting to {broker}:{port} as {username}...")

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("✅ Connected to MQTT broker"))
                client.subscribe(topic)
                self.stdout.write(f"📡 Subscribed to {topic}")
            else:
                self.stdout.write(self.style.ERROR(f"❌ Connection failed with code {rc}"))
                # rc meanings:
                # 1: incorrect protocol version
                # 2: invalid client ID
                # 3: server unavailable
                # 4: bad username/password
                # 5: not authorised

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()
                self.stdout.write(f"📥 Received: {payload} on {msg.topic}")

                # Save to database – adjust to your model
                RFIDScan.objects.create(
                    rfid_tag=payload,
                    rfid=None,
                    payload={"topic": msg.topic, "payload": payload, "qos": msg.qos},
                    created_at=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS("💾 Saved to database"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"⚠️ Error processing message: {e}"))

        def on_disconnect(client, userdata, rc):
            self.stdout.write(self.style.WARNING(f"🔌 Disconnected (rc: {rc})"))

        # Create MQTT client
        client = mqtt.Client()
        client.username_pw_set(username, password)
        client.tls_set()  # Uses system CA certs

        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        try:
            client.connect(broker, port, 60)
            client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.NOTICE("🛑 Stopping subscriber..."))
            client.disconnect()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"🔥 Fatal error: {e}"))