import os
import qrcode
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from core.models import Table


class Command(BaseCommand):
    help = 'Barcha stollar uchun QR kodlar yaratadi'

    def handle(self, *args, **options):
        tables = Table.objects.all()
        site_url = 'http://localhost:8000'

        for table in tables:
            url = f'{site_url}/menu/{table.id}/'

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            filename = f'qr_codes/table_{table.number}.png'
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            table.qr_code.save(filename, File(buffer), save=True)

            self.stdout.write(
                self.style.SUCCESS(f'Stol #{table.number} uchun QR kod yaratildi: {url}')
            )

        self.stdout.write(self.style.SUCCESS(f'{tables.count()} ta stol uchun QR kodlar yaratildi!'))
