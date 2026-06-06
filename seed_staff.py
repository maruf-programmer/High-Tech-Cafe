import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')

import django
django.setup()

from core.models import Staff, Table
from orders.models import WaiterCall

# Xodimlar qo'shish
if not Staff.objects.exists():
    staff_list = [
        {'name': 'Aliyev Sarvar', 'phone': '+998901234567', 'role': 'waiter'},
        {'name': 'Karimova Dilnoza', 'phone': '+998901234568', 'role': 'waiter'},
        {'name': 'Toshmatov Bekzod', 'phone': '+998901234569', 'role': 'chef'},
        {'name': 'Saidova Mohira', 'phone': '+998901234570', 'role': 'admin'},
        {'name': 'Rahimov Olim', 'phone': '+998901234571', 'role': 'cleaner'},
    ]
    for s in staff_list:
        Staff.objects.create(**s)
    print('5 ta xodim qo\'shildi!')

# Stollar uchun sessiya vaqtini yangilash
tables = Table.objects.filter(status='occupied', current_session_start__isnull=True)
for t in tables:
    from django.utils import timezone
    t.current_session_start = timezone.now()
    t.save()
print('Stollar yangilandi!')

print('Barcha ma\'lumotlar tayyor!')
