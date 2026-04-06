# LuxeStay — Premium Hotel Room Booking Website

A full-featured hotel room booking website built using Python Django and SQLite.

## Overview

### Existing Problem
Many hotel booking systems are either too complex for small-to-medium luxury hotels or lack the premium aesthetic required to sell high-end experiences. Existing solutions often involve complicated database setups and clunky user interfaces that don't reflect the luxury of the properties they represent.

### Proposed Solution
LuxeStay is a streamlined, premium hotel booking application built with Django. It provides a seamless, visually stunning experience for guests while remaining incredibly easy to deploy and manage for hotel owners. 

By leveraging Django and SQLite, the application requires minimal infrastructure setup while delivering essential features:
- **Premium Aesthetics:** A dark-luxury theme with glassmorphism, gold accents, and smooth scroll animations.
- **Robust Booking Engine:** Real-time availability checking, date validation (preventing double bookings), and dynamic price calculation.
- **Streamlined Management:** Easy-to-use Django Admin panel to manage rooms, bookings, and customer inquiries.

## Key Features

- **Room Browsing & Filtering:** Guests can filter rooms by type, capacity, and available dates.
- **Dynamic Pricing & Validation:** Total price is calculated dynamically based on selected dates. Form validation ensures check-out is after check-in and prevents past-date bookings.
- **Automated Reference Codes:** Each confirmed booking generates a unique alphanumeric reference code.
- **Seed Data:** Includes a script (`booking/seed.py`) to instantly populate the database with realistic sample rooms (Standard, Deluxe, Suite, Penthouse).
- **Responsive Design:** Fully responsive layout ensuring a premium experience on both mobile and desktop devices.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML, Vanilla CSS (Custom properties, Flexbox, Grid), Vanilla JavaScript

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Austameer/hotel-room-booking.git
   cd "hotel-room-booking"
   ```

2. **Install dependencies:**
   ```bash
   pip install django
   ```

3. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Seed the database with sample rooms:**
   ```bash
   python booking/seed.py
   ```

5. **Create an admin user (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/` in your browser.
