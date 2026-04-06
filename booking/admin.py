from django.contrib import admin
from .models import Room, Booking, ContactMessage


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price_per_night', 'capacity', 'is_available', 'is_featured')
    list_filter = ('room_type', 'is_available', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'is_featured', 'price_per_night')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ref', 'guest_name', 'room', 'check_in', 'check_out', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'check_in', 'created_at')
    search_fields = ('booking_ref', 'guest_name', 'guest_email')
    readonly_fields = ('booking_ref', 'created_at')
    list_editable = ('status',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
