from django import forms
from django.utils import timezone
from .models import Booking, ContactMessage, Review


class SearchForm(forms.Form):
    check_in = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input',
            'id': 'search-checkin',
        })
    )
    check_out = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input',
            'id': 'search-checkout',
        })
    )
    guests = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Guests',
            'id': 'search-guests',
        })
    )
    room_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types'), ('standard', 'Standard'), ('deluxe', 'Deluxe'), ('suite', 'Suite'), ('penthouse', 'Penthouse')],
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'search-room-type',
        })
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out', 'num_guests', 'special_requests']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Full Name',
                'id': 'booking-name',
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email Address',
                'id': 'booking-email',
            }),
            'guest_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone Number',
                'id': 'booking-phone',
            }),
            'check_in': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
                'id': 'booking-checkin',
            }),
            'check_out': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
                'id': 'booking-checkout',
            }),
            'num_guests': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'id': 'booking-guests',
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Any special requests...',
                'id': 'booking-requests',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            today = timezone.now().date()
            if check_in < today:
                raise forms.ValidationError("Check-in date cannot be in the past.")
            if check_out <= check_in:
                raise forms.ValidationError("Check-out date must be after check-in date.")
            if (check_out - check_in).days > 30:
                raise forms.ValidationError("Maximum booking duration is 30 days.")

        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name',
                'id': 'contact-name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Email',
                'id': 'contact-email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject',
                'id': 'contact-subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': 'Your Message...',
                'id': 'contact-message',
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['guest_name', 'guest_email', 'rating', 'comment']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name',
                'id': 'review-name',
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Email',
                'id': 'review-email',
            }),
            'rating': forms.HiddenInput(attrs={
                'id': 'review-rating-value',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Share your experience...',
                'id': 'review-comment',
            }),
        }


class BookingLookupForm(forms.Form):
    booking_ref = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. A1B2C3D4E5',
            'id': 'lookup-ref',
            'style': 'text-transform: uppercase; letter-spacing: 2px;',
        })
    )
    guest_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email used during booking',
            'id': 'lookup-email',
        })
    )
