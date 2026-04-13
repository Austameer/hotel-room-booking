from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking/confirm/<str:booking_ref>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-booking/', views.booking_lookup, name='booking_lookup'),
    path('cancel-booking/<str:booking_ref>/', views.cancel_booking, name='cancel_booking'),
    path('gallery/', views.gallery, name='gallery'),
    path('offers/', views.offers, name='offers'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
]
