# yourapp/management/commands/add_fake_scans.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import RFIDScan
import json
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Add fake RFID scan data'

    def handle(self, *args, **options):
        base_time = timezone.now()
        for i in range(1, 11):
            tag = f"TAG-{i:05d}"
            payload = {
                "topic": "/transaction",
                "payload": tag,
                "qos": 1,
                "clientid": f"publisher-{random.randint(1000,9999)}"
            }
            RFIDScan.objects.create(
                rfid_tag=tag,
                rfid=None,
                payload=payload,
                created_at=base_time - timedelta(minutes=i*5)
            )
        self.stdout.write(self.style.SUCCESS('Added 10 fake scans'))