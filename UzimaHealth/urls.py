from django.urls import path
from . import views

app_name = 'UzimaHealth'  # Application namespace

urlpatterns = [ 
    path('', views.Home_page, name='Home'),  # Home page
    path('about/', views.about_page, name='about'),  # About page
    path('departments/', views.departments_page, name='departments'),  # Departments page
    path('services/', views.services_page, name='services'),  # Services page
    path('contact/', views.contact_page, name='contact'),  # Contact page
    path('booking/', views.booking_page, name='booking'),  # Booking page
    path('show_booking/', views.show_booking_page, name='show_booking'),  # Show Booking page
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),  # Delete Booking
    path('update_booking/<int:booking_id>/', views.update_booking, name='update_booking'),  # Update Booking
]