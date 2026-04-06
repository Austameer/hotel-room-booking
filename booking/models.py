import uuid
from django.db import models
from django.utils import timezone


class Room(models.Model):
    ROOM_TYPES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        ('penthouse', 'Penthouse'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='standard')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=2)
    size_sqft = models.IntegerField(default=300)
    description = models.TextField()
    amenities = models.TextField(help_text="Comma-separated list of amenities")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price_per_night']

    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"

    def get_amenities_list(self):
        return [a.strip() for a in self.amenities.split(',') if a.strip()]

    def is_available_for_dates(self, check_in, check_out):
        """Check if this room is available for the given date range."""
        overlapping = self.bookings.filter(
            status__in=['pending', 'confirmed'],
            check_in__lt=check_out,
            check_out__gt=check_in,
        )
        return not overlapping.exists()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booking_ref = models.CharField(max_length=12, unique=True, editable=False)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_ref} - {self.guest_name}"

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = uuid.uuid4().hex[:10].upper()
        if not self.total_price:
            nights = (self.check_out - self.check_in).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)

    @property
    def num_nights(self):
        return (self.check_out - self.check_in).days


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"
