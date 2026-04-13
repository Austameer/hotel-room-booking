from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from booking.models import Room, Review, Offer, GalleryImage


class Command(BaseCommand):
    help = 'Seed gallery images, offers, and sample reviews'

    def handle(self, *args, **options):
        # --- Gallery Images (using Unsplash) ---
        gallery_data = [
            {'title': 'Grand Lobby Entrance', 'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800', 'category': 'lobby', 'ordering': 1},
            {'title': 'Crystal Chandelier Lobby', 'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800', 'category': 'lobby', 'ordering': 2},
            {'title': 'Luxury Suite Bedroom', 'image_url': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800', 'category': 'rooms', 'ordering': 3},
            {'title': 'Premium King Room', 'image_url': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800', 'category': 'rooms', 'ordering': 4},
            {'title': 'Deluxe Twin Room', 'image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800', 'category': 'rooms', 'ordering': 5},
            {'title': 'Penthouse Living Area', 'image_url': 'https://images.unsplash.com/photo-1590490360182-c33d955e5b7c?w=800', 'category': 'rooms', 'ordering': 6},
            {'title': 'Rooftop Infinity Pool', 'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800', 'category': 'pool', 'ordering': 7},
            {'title': 'Poolside Lounge', 'image_url': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800', 'category': 'pool', 'ordering': 8},
            {'title': 'Spa Treatment Room', 'image_url': 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800', 'category': 'pool', 'ordering': 9},
            {'title': 'Fine Dining Restaurant', 'image_url': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800', 'category': 'dining', 'ordering': 10},
            {'title': 'Breakfast Buffet', 'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800', 'category': 'dining', 'ordering': 11},
            {'title': 'Rooftop Bar', 'image_url': 'https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=800', 'category': 'dining', 'ordering': 12},
            {'title': 'Hotel Exterior Night', 'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800', 'category': 'exterior', 'ordering': 13},
            {'title': 'Garden Pathway', 'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800', 'category': 'exterior', 'ordering': 14},
            {'title': 'Hotel Facade Daytime', 'image_url': 'https://images.unsplash.com/photo-1455587734955-081b22074882?w=800', 'category': 'exterior', 'ordering': 15},
        ]

        GalleryImage.objects.all().delete()
        for data in gallery_data:
            GalleryImage.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(gallery_data)} gallery images'))

        # --- Offers ---
        now = timezone.now()
        offers_data = [
            {
                'title': 'Early Bird Summer Special',
                'description': 'Book your summer getaway in advance and enjoy an exclusive 25% discount on all room types. Perfect for planning that dream holiday.',
                'discount_percent': 25,
                'promo_code': 'SUMMER25',
                'valid_from': now,
                'valid_to': now + timedelta(days=30),
                'room_type': None,
                'is_active': True,
            },
            {
                'title': 'Suite Upgrade Weekend',
                'description': 'Experience the ultimate luxury with 30% off all Suite bookings. Indulge in spacious living areas and premium amenities this weekend.',
                'discount_percent': 30,
                'promo_code': 'SUITE30',
                'valid_from': now,
                'valid_to': now + timedelta(days=14),
                'room_type': 'suite',
                'is_active': True,
            },
            {
                'title': 'Penthouse Experience',
                'description': 'Live like royalty with our exclusive Penthouse offer. Enjoy breathtaking views, private butler service, and world-class dining at 20% off.',
                'discount_percent': 20,
                'promo_code': 'PENT20',
                'valid_from': now,
                'valid_to': now + timedelta(days=45),
                'room_type': 'penthouse',
                'is_active': True,
            },
            {
                'title': 'Extended Stay Savings',
                'description': 'Stay 5 nights or more and unlock 15% savings on your entire reservation. The longer you stay, the more you save.',
                'discount_percent': 15,
                'promo_code': 'STAY15',
                'valid_from': now,
                'valid_to': now + timedelta(days=60),
                'room_type': None,
                'is_active': True,
            },
        ]

        Offer.objects.all().delete()
        for data in offers_data:
            Offer.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(offers_data)} offers'))

        # --- Sample Reviews ---
        rooms = Room.objects.all()
        reviews_data = [
            {'guest_name': 'Priya Sharma', 'guest_email': 'priya@example.com', 'rating': 5, 'comment': 'Absolutely stunning hotel! The room was immaculate, the staff was incredibly attentive, and the views were breathtaking. Will definitely be coming back.'},
            {'guest_name': 'Rahul Verma', 'guest_email': 'rahul@example.com', 'rating': 4, 'comment': 'Great experience overall. The room was spacious and comfortable. The only minor issue was the Wi-Fi speed, but everything else was perfect.'},
            {'guest_name': 'Anita Patel', 'guest_email': 'anita@example.com', 'rating': 5, 'comment': 'LuxeStay exceeded all our expectations! The spa was heavenly, and the rooftop pool is a must-try. Perfect for a romantic getaway.'},
            {'guest_name': 'Vikram Singh', 'guest_email': 'vikram@example.com', 'rating': 4, 'comment': 'Very professional staff and beautiful interiors. Breakfast buffet had amazing variety. Highly recommend the deluxe rooms.'},
            {'guest_name': 'Meera Kapoor', 'guest_email': 'meera@example.com', 'rating': 5, 'comment': 'One of the best hotels I have ever stayed at. The attention to detail is remarkable. The concierge helped us plan our entire trip.'},
            {'guest_name': 'Arjun Nair', 'guest_email': 'arjun@example.com', 'rating': 3, 'comment': 'Decent stay. Room was clean and well-maintained. Location is excellent. Would have appreciated later checkout options though.'},
        ]

        Review.objects.all().delete()
        for i, room in enumerate(rooms):
            # Give each room 2 reviews
            for j in range(2):
                idx = (i * 2 + j) % len(reviews_data)
                Review.objects.create(room=room, **reviews_data[idx])
        self.stdout.write(self.style.SUCCESS(f'Created sample reviews for {rooms.count()} rooms'))

        self.stdout.write(self.style.SUCCESS('All seed data created successfully!'))
