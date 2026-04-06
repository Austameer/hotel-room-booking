"""
Seed script to populate sample rooms.
Run with: python manage.py shell < booking/seed.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from booking.models import Room

# Clear existing rooms
Room.objects.all().delete()

rooms_data = [
    {
        'name': 'Oceanview Standard',
        'room_type': 'standard',
        'price_per_night': 4500,
        'capacity': 2,
        'size_sqft': 320,
        'description': 'A comfortable and elegantly appointed room featuring modern amenities and serene ocean views. Perfect for couples seeking a relaxing getaway with all the essentials for a memorable stay.',
        'amenities': 'Free Wi-Fi, Air Conditioning, Flat Screen TV, Mini Bar, Room Service, Daily Housekeeping, Coffee Maker, In-Room Safe',
        'is_available': True,
        'is_featured': False,
    },
    {
        'name': 'Garden View Standard',
        'room_type': 'standard',
        'price_per_night': 3800,
        'capacity': 2,
        'size_sqft': 300,
        'description': 'Wake up to beautiful garden views in this cozy standard room. Features contemporary decor and all the comforts you need for a pleasant stay.',
        'amenities': 'Free Wi-Fi, Air Conditioning, Flat Screen TV, Room Service, Daily Housekeeping, Coffee Maker, Iron & Ironing Board',
        'is_available': True,
        'is_featured': False,
    },
    {
        'name': 'Sunset Deluxe Room',
        'room_type': 'deluxe',
        'price_per_night': 7500,
        'capacity': 3,
        'size_sqft': 480,
        'description': 'Spacious and luxuriously furnished, our Deluxe Room offers stunning sunset views with premium bedding, a sitting area, and top-tier amenities for the discerning traveler.',
        'amenities': 'Free Wi-Fi, Air Conditioning, 55-inch Smart TV, Mini Bar, Espresso Machine, Bathrobe & Slippers, Rain Shower, Room Service, Balcony, Complimentary Breakfast',
        'is_available': True,
        'is_featured': True,
    },
    {
        'name': 'City Lights Deluxe',
        'room_type': 'deluxe',
        'price_per_night': 8200,
        'capacity': 3,
        'size_sqft': 520,
        'description': 'Experience the magic of city nightlife from the comfort of your Deluxe Room. Floor-to-ceiling windows frame spectacular city views while you enjoy premium furnishings.',
        'amenities': 'Free Wi-Fi, Air Conditioning, 55-inch Smart TV, Premium Mini Bar, Nespresso Machine, Bathrobe & Slippers, Jacuzzi Tub, Room Service, Private Balcony, Complimentary Breakfast, Turndown Service',
        'is_available': True,
        'is_featured': True,
    },
    {
        'name': 'Royal Heritage Suite',
        'room_type': 'suite',
        'price_per_night': 15000,
        'capacity': 4,
        'size_sqft': 800,
        'description': 'Our signature suite combines traditional elegance with modern luxury. Features a separate living room, dining area, and bedroom with the finest furnishings and panoramic views.',
        'amenities': 'Free Wi-Fi, Central AC, 65-inch Smart TV, Full Bar, Espresso Machine, Premium Bathrobe, Jacuzzi, 24/7 Butler Service, Private Terrace, All Meals Included, Spa Access, Lounge Access, Workstation, Sound System',
        'is_available': True,
        'is_featured': True,
    },
    {
        'name': 'Ambassador Suite',
        'room_type': 'suite',
        'price_per_night': 18000,
        'capacity': 4,
        'size_sqft': 950,
        'description': 'The Ambassador Suite is the epitome of sophistication. With two bedrooms, a full kitchen, and a grand living space, it offers an unparalleled residential experience.',
        'amenities': 'Free Wi-Fi, Central AC, Two 65-inch Smart TVs, Full Bar, Kitchen, Premium Linens, Steam Shower, 24/7 Butler, Wraparound Terrace, All Meals, Spa Access, Airport Transfer, Personal Chef on Request',
        'is_available': True,
        'is_featured': False,
    },
    {
        'name': 'The Grand Penthouse',
        'room_type': 'penthouse',
        'price_per_night': 35000,
        'capacity': 6,
        'size_sqft': 1800,
        'description': 'The crown jewel of LuxeStay. This magnificent penthouse spans the entire top floor with 360° views, private infinity pool, home theater, and bespoke luxury in every detail.',
        'amenities': 'Free Wi-Fi, Smart Home System, Home Theater, Private Pool, Full Gourmet Kitchen, Wine Cellar, Steam & Sauna, 24/7 Dedicated Staff, Helipad Access, Rolls-Royce Transfer, Private Dining, All Inclusive',
        'is_available': True,
        'is_featured': False,
    },
    {
        'name': 'Family Comfort Room',
        'room_type': 'standard',
        'price_per_night': 5500,
        'capacity': 4,
        'size_sqft': 420,
        'description': 'Designed with families in mind, this spacious room offers two queen beds, a play area, and child-friendly amenities for a comfortable family vacation.',
        'amenities': 'Free Wi-Fi, Air Conditioning, Flat Screen TV, Mini Fridge, Room Service, Daily Housekeeping, Baby Cot Available, Kids Amenity Kit, Board Games',
        'is_available': True,
        'is_featured': False,
    },
]

for data in rooms_data:
    Room.objects.create(**data)

print(f"✅ Successfully created {len(rooms_data)} rooms!")
print("Rooms:")
for room in Room.objects.all():
    print(f"  • {room.name} — ₹{room.price_per_night}/night ({room.get_room_type_display()})")
