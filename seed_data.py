import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from core.models import Table, Category, MenuItem, Advertisement

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@cafe.uz', 'admin123')
    print('Superuser yaratildi: admin / admin123')

if not Table.objects.exists():
    for i in range(1, 11):
        Table.objects.create(number=i)
    print('10 ta stol yaratildi')

if not Category.objects.exists():
    categories = [
        {'name': "Salatlar", 'description': "Yangi va mazali salatlar", 'prep_time_minutes': 10, 'order': 1},
        {'name': "Sho'rvalar", 'description': "Issiq va mazali sho'rvalar", 'prep_time_minutes': 20, 'order': 2},
        {'name': "Asosiy taomlar", 'description': "To'yimli asosiy taomlar", 'prep_time_minutes': 30, 'order': 3},
        {'name': "Go'sht taomlari", 'description': "Mazali go'shtli taomlar", 'prep_time_minutes': 40, 'order': 4},
        {'name': "Ichimliklar", 'description': "Sovuq va issiq ichimliklar", 'prep_time_minutes': 5, 'order': 5},
        {'name': "Desertlar", 'description': "Shirin va mazali desertlar", 'prep_time_minutes': 15, 'order': 6},
    ]
    for cat in categories:
        Category.objects.create(**cat)
    print('Kategoriyalar yaratildi')

if not MenuItem.objects.exists():
    salads_cat = Category.objects.get(name="Salatlar")
    soups_cat = Category.objects.get(name="Sho'rvalar")
    main_cat = Category.objects.get(name="Asosiy taomlar")
    meat_cat = Category.objects.get(name="Go'sht taomlari")
    drinks_cat = Category.objects.get(name="Ichimliklar")
    desserts_cat = Category.objects.get(name="Desertlar")

    menu_items = [
        {"name": "Sezar salati", "description": "Roma salat, tovuq go'shti, parmezan pishloq, krutonlar, Sezar sousi bilan.", "category": salads_cat, "price": 45000, "prep_time_minutes": 10, "weight_grams": 250, "calories": 320, "ingredients": "Roma salat, tovuq, parmezan, kruton, Sezar sousi", "vitamins": "A, C, K, B6, B12", "is_popular": True, "serving_options": [1, 2, 3]},
        {"name": "Yunon salati", "description": "Pomidor, bodring, zaytun, feta pishloq, zaytun moyi bilan.", "category": salads_cat, "price": 38000, "prep_time_minutes": 8, "weight_grams": 300, "calories": 280, "ingredients": "Pomidor, bodring, zaytun, feta, zaytun moyi", "vitamins": "A, C, E, K", "serving_options": [1, 2]},
        {"name": "Lag'mon", "description": "An'anaviy o'zbek lag'moni — qo'lda tortilgan noodle, sabzavotlar va mol go'shti bilan.", "category": soups_cat, "price": 55000, "prep_time_minutes": 30, "weight_grams": 450, "calories": 520, "ingredients": "Noodle, mol go'shti, kartoshka, sabzi, piyoz, pomidor", "vitamins": "A, B1, B2, B6, C, D", "is_popular": True, "serving_options": [1, 2, 3]},
        {"name": "Sho'rva", "description": "Mol go'shti va sabzavotlar bilan tayyorlangan an'anaviy sho'rva.", "category": soups_cat, "price": 35000, "prep_time_minutes": 25, "weight_grams": 350, "calories": 280, "ingredients": "Mol go'shti, kartoshka, sabzi, piyoz, tuz, murch", "vitamins": "A, B6, B12, C, D", "serving_options": [1, 2]},
        {"name": "Osh (Palov)", "description": "O'zbek palovi — guruch, mol go'shti, sabzi, zira va boshqa ziravorlar bilan.", "category": main_cat, "price": 50000, "prep_time_minutes": 40, "weight_grams": 400, "calories": 650, "ingredients": "Guruch, mol go'shti, sabzi, piyoz, zira, tuz, murch", "vitamins": "A, B1, B6, B12, C, D, E", "is_popular": True, "serving_options": [1, 2, 3, 4, 5]},
        {"name": "Manti", "description": "Qo'lda yopilgan manti — mol go'shti, piyoz va ziravorlar bilan.", "category": main_cat, "price": 45000, "prep_time_minutes": 35, "weight_grams": 350, "calories": 480, "ingredients": "Un, mol go'shti, piyoz, tuz, murch, qatiq sousi", "vitamins": "B1, B2, B6, B12, D", "serving_options": [1, 2, 3]},
        {"name": "Chuchvara", "description": "Kichik chuchvara — mol go'shti va sabzavotlar bilan.", "category": main_cat, "price": 40000, "prep_time_minutes": 30, "weight_grams": 300, "calories": 380, "ingredients": "Un, mol go'shti, sabzavotlar, piyoz, tuz, murch", "vitamins": "B1, B6, B12, C", "serving_options": [1, 2]},
        {"name": "Shashlik", "description": "Mol go'shtidan tayyorlangan shashlik — ko'mirda pishirilgan.", "category": meat_cat, "price": 65000, "prep_time_minutes": 25, "weight_grams": 300, "calories": 420, "ingredients": "Mol go'shti, piyoz, ziravorlar, ko'mir", "vitamins": "B6, B12, D, E", "is_popular": True, "serving_options": [1, 2, 3]},
        {"name": "Tovuq kabob", "description": "Tovuq go'shtidan tayyorlangan kabob — maxsus marinad bilan.", "category": meat_cat, "price": 55000, "prep_time_minutes": 20, "weight_grams": 280, "calories": 350, "ingredients": "Tovuq go'shti, limon, sarimsoq, ziravorlar", "vitamins": "B3, B6, B12, D", "serving_options": [1, 2]},
        {"name": "Yashil choy", "description": "An'anaviy o'zbek yashil choyi.", "category": drinks_cat, "price": 8000, "prep_time_minutes": 5, "weight_grams": 300, "calories": 2, "ingredients": "Yashil choy barglari, suv", "vitamins": "C, E, K", "serving_options": [1, 2]},
        {"name": "Qora choy", "description": "An'anaviy qora choy.", "category": drinks_cat, "price": 7000, "prep_time_minutes": 5, "weight_grams": 300, "calories": 2, "ingredients": "Qora choy barglari, suv", "vitamins": "B2, B3", "serving_options": [1, 2]},
        {"name": "Limonad", "description": "Uy sharoitida tayyorlangan yangi limonad.", "category": drinks_cat, "price": 15000, "prep_time_minutes": 5, "weight_grams": 400, "calories": 120, "ingredients": "Limon, shakar, suv, yalpiz", "vitamins": "C, B6", "serving_options": [1, 2]},
        {"name": "Medovik tort", "description": "An'anaviy medovik — asal va qaymoq bilan.", "category": desserts_cat, "price": 30000, "prep_time_minutes": 10, "weight_grams": 150, "calories": 380, "ingredients": "Un, asal, tuxum, qaymoq, shakar", "vitamins": "A, B2, D, E", "serving_options": [1]},
        {"name": "Paxlava", "description": "An'anaviy o'zbek paxlavasi — yong'oq va asal bilan.", "category": desserts_cat, "price": 25000, "prep_time_minutes": 5, "weight_grams": 120, "calories": 420, "ingredients": "Un, yong'oq, asal, shakar, sariyog'", "vitamins": "E, B1, B6", "serving_options": [1, 2]},
    ]

    for item in menu_items:
        MenuItem.objects.create(**item)
    print('14 ta taom yaratildi')

if not Advertisement.objects.exists():
    Advertisement.objects.create(
        title="Yangi mijozlar uchun 20% chegirma!",
        description="Birinchi tashrifingizda barcha taomlarga 20% chegirma",
    )
    Advertisement.objects.create(
        title="Oila uchun maxsus taklif",
        description="4 kishilik buyurtmaga 1 ta desert bepul!",
    )
    print('Reklamalar yaratildi')

print('Barcha namuna ma\'lumotlar yaratildi!')
