from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Room, Booking, ContactMessage
from .forms import SearchForm, BookingForm, ContactForm


def home(request):
    """Landing page with hero section, search, and featured rooms."""
    featured_rooms = Room.objects.filter(is_featured=True, is_available=True)[:3]
    all_rooms = Room.objects.filter(is_available=True)[:6]
    search_form = SearchForm()
    context = {
        'featured_rooms': featured_rooms,
        'all_rooms': all_rooms,
        'search_form': search_form,
    }
    return render(request, 'home.html', context)


def room_list(request):
    """Room listing page with search and filter functionality."""
    rooms = Room.objects.filter(is_available=True)
    search_form = SearchForm(request.GET or None)

    check_in = None
    check_out = None

    if search_form.is_valid():
        check_in = search_form.cleaned_data.get('check_in')
        check_out = search_form.cleaned_data.get('check_out')
        guests = search_form.cleaned_data.get('guests')
        room_type = search_form.cleaned_data.get('room_type')

        if guests:
            rooms = rooms.filter(capacity__gte=guests)
        if room_type:
            rooms = rooms.filter(room_type=room_type)
        if check_in and check_out:
            unavailable_rooms = Booking.objects.filter(
                status__in=['pending', 'confirmed'],
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).values_list('room_id', flat=True)
            rooms = rooms.exclude(id__in=unavailable_rooms)

    context = {
        'rooms': rooms,
        'search_form': search_form,
        'check_in': check_in,
        'check_out': check_out,
    }
    return render(request, 'rooms.html', context)


def room_detail(request, room_id):
    """Single room detail page."""
    room = get_object_or_404(Room, id=room_id)
    context = {
        'room': room,
        'amenities': room.get_amenities_list(),
    }
    return render(request, 'room_detail.html', context)


def book_room(request, room_id):
    """Booking form page for a specific room."""
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room

            # Check if room is available for selected dates
            if not room.is_available_for_dates(booking.check_in, booking.check_out):
                messages.error(request, 'Sorry, this room is not available for the selected dates. Please choose different dates.')
                return render(request, 'booking_form.html', {'form': form, 'room': room})

            # Check capacity
            if booking.num_guests > room.capacity:
                messages.error(request, f'This room can accommodate a maximum of {room.capacity} guests.')
                return render(request, 'booking_form.html', {'form': form, 'room': room})

            # Calculate total price
            nights = (booking.check_out - booking.check_in).days
            booking.total_price = room.price_per_night * nights
            booking.save()

            messages.success(request, 'Your booking has been confirmed!')
            return redirect('booking_confirmation', booking_ref=booking.booking_ref)
    else:
        initial = {}
        if request.GET.get('check_in'):
            initial['check_in'] = request.GET['check_in']
        if request.GET.get('check_out'):
            initial['check_out'] = request.GET['check_out']
        form = BookingForm(initial=initial)

    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'booking_form.html', context)


def booking_confirmation(request, booking_ref):
    """Booking confirmation page."""
    booking = get_object_or_404(Booking, booking_ref=booking_ref)
    context = {
        'booking': booking,
    }
    return render(request, 'booking_confirm.html', context)


def contact(request):
    """Contact page with form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)
