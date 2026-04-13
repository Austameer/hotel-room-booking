from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from .models import Room, Booking, ContactMessage, Review, Offer, GalleryImage
from .forms import SearchForm, BookingForm, ContactForm, ReviewForm, BookingLookupForm


def home(request):
    """Landing page with hero section, search, and featured rooms."""
    featured_rooms = Room.objects.filter(is_featured=True, is_available=True)[:3]
    all_rooms = Room.objects.filter(is_available=True)[:6]
    search_form = SearchForm()

    # Annotate rooms with average rating
    for room in featured_rooms:
        avg = room.reviews.aggregate(Avg('rating'))['rating__avg']
        room.avg_rating = round(avg, 1) if avg else None
        room.review_count = room.reviews.count()

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

    # Annotate rooms with average rating
    for room in rooms:
        avg = room.reviews.aggregate(Avg('rating'))['rating__avg']
        room.avg_rating = round(avg, 1) if avg else None
        room.review_count = room.reviews.count()

    context = {
        'rooms': rooms,
        'search_form': search_form,
        'check_in': check_in,
        'check_out': check_out,
    }
    return render(request, 'rooms.html', context)


def room_detail(request, room_id):
    """Single room detail page with reviews."""
    room = get_object_or_404(Room, id=room_id)
    reviews = room.reviews.all()[:10]
    avg_rating = room.reviews.aggregate(Avg('rating'))['rating__avg']
    review_count = room.reviews.count()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.room = room
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('room_detail', room_id=room.id)
    else:
        review_form = ReviewForm()

    context = {
        'room': room,
        'amenities': room.get_amenities_list(),
        'reviews': reviews,
        'review_form': review_form,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'review_count': review_count,
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


def booking_lookup(request):
    """Booking lookup page — find and manage your booking."""
    booking = None
    not_found = False

    if request.method == 'POST':
        form = BookingLookupForm(request.POST)
        if form.is_valid():
            ref = form.cleaned_data['booking_ref'].strip().upper()
            email = form.cleaned_data['guest_email'].strip().lower()
            try:
                booking = Booking.objects.get(booking_ref=ref, guest_email__iexact=email)
            except Booking.DoesNotExist:
                not_found = True
    else:
        form = BookingLookupForm()

    context = {
        'form': form,
        'booking': booking,
        'not_found': not_found,
    }
    return render(request, 'booking_lookup.html', context)


def cancel_booking(request, booking_ref):
    """Cancel a booking by reference code."""
    if request.method == 'POST':
        email = request.POST.get('guest_email', '').strip().lower()
        try:
            booking = Booking.objects.get(booking_ref=booking_ref, guest_email__iexact=email)
            if booking.status in ['pending', 'confirmed']:
                booking.status = 'cancelled'
                booking.save()
                messages.success(request, f'Booking {booking_ref} has been cancelled successfully.')
            else:
                messages.error(request, 'This booking cannot be cancelled.')
        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')
    return redirect('booking_lookup')


def gallery(request):
    """Photo gallery page."""
    images = GalleryImage.objects.all()
    categories = GalleryImage.CATEGORY_CHOICES
    context = {
        'images': images,
        'categories': categories,
    }
    return render(request, 'gallery.html', context)


def offers(request):
    """Special offers page."""
    now = timezone.now()
    active_offers = Offer.objects.filter(is_active=True, valid_to__gte=now)
    context = {
        'offers': active_offers,
    }
    return render(request, 'offers.html', context)


def faq(request):
    """FAQ / Help page."""
    faqs = [
        {
            'category': 'Booking',
            'items': [
                {'q': 'How do I make a reservation?', 'a': 'Browse our rooms, select your preferred room, choose your dates, fill in your details, and confirm your booking. You\'ll receive a booking reference immediately.'},
                {'q': 'Can I book multiple rooms at once?', 'a': 'Currently, each room must be booked separately. Simply complete one booking and start another for additional rooms.'},
                {'q': 'How far in advance can I book?', 'a': 'You can book up to 6 months in advance. We recommend booking early during peak seasons to secure your preferred room.'},
                {'q': 'Do I need to create an account to book?', 'a': 'No account is needed. Simply provide your name, email, and phone number during the booking process.'},
            ]
        },
        {
            'category': 'Payment',
            'items': [
                {'q': 'What payment methods do you accept?', 'a': 'We accept all major credit and debit cards, UPI payments, net banking, and digital wallets including Paytm, PhonePe, and Google Pay.'},
                {'q': 'Is payment required at the time of booking?', 'a': 'A confirmation is generated immediately. Payment can be made at check-in or through our secure payment gateway online.'},
                {'q': 'Are there any hidden charges?', 'a': 'No, the price displayed includes all applicable taxes. Additional services like room service, laundry, or minibar are charged separately.'},
            ]
        },
        {
            'category': 'Cancellation',
            'items': [
                {'q': 'What is your cancellation policy?', 'a': 'Free cancellation is available up to 24 hours before your check-in date. Cancellations made within 24 hours may be subject to a one-night charge.'},
                {'q': 'How do I cancel my booking?', 'a': 'Visit the "My Booking" page, enter your booking reference and email, and click the cancel button. You\'ll receive a confirmation of cancellation.'},
                {'q': 'Will I get a refund after cancellation?', 'a': 'For free cancellations (24+ hours before check-in), a full refund is processed within 5-7 business days to the original payment method.'},
            ]
        },
        {
            'category': 'Amenities',
            'items': [
                {'q': 'What amenities are included?', 'a': 'All rooms include complimentary Wi-Fi, air conditioning, flat-screen TV, minibar, and an in-room safe. Premium rooms offer additional luxuries.'},
                {'q': 'Do you have a swimming pool?', 'a': 'Yes! We feature a stunning rooftop infinity pool open from 6 AM to 10 PM daily, with poolside bar service available.'},
                {'q': 'Is breakfast included?', 'a': 'Complimentary breakfast buffet is included with Deluxe, Suite, and Penthouse bookings. Standard room guests can add breakfast for ₹500 per person.'},
                {'q': 'Do you offer airport transfers?', 'a': 'Yes, we offer luxury airport transfer services. Please mention this in your special requests during booking or contact our concierge.'},
            ]
        },
        {
            'category': 'General',
            'items': [
                {'q': 'What are your check-in and check-out times?', 'a': 'Check-in is at 2:00 PM and check-out is at 12:00 PM (noon). Early check-in and late check-out may be available upon request.'},
                {'q': 'Is parking available?', 'a': 'Yes, we offer complimentary valet parking for all guests. Self-parking is also available in our secure underground garage.'},
                {'q': 'Are pets allowed?', 'a': 'We welcome small pets (under 10 kg) in select pet-friendly rooms. An additional pet fee of ₹1,000 per night applies. Please inform us during booking.'},
                {'q': 'Do you cater to special occasions?', 'a': 'Absolutely! We offer special packages for birthdays, anniversaries, and honeymoons. Contact our events team for custom arrangements.'},
            ]
        },
    ]
    context = {
        'faq_categories': faqs,
    }
    return render(request, 'faq.html', context)


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
