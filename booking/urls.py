from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking/confirm/<str:booking_ref>/', views.booking_confirmation, name='booking_confirmation'),
    path('contact/', views.contact, name='contact'),
]
