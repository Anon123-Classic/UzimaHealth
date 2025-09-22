from django.shortcuts import render, redirect
from .models import Bookings
from .models import Contact
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import uuid





# Create your views here.

def Home_page(request):
    return render(request, 'index.html') # Render the home page template
def about_page(request):
    return render(request, 'about.html') # Render the about page template
def departments_page(request):
    return render(request, 'departments.html') # Render the departments page template
def services_page(request):
    return render(request, 'services.html') # Render the services page template
def contact_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save to DB
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("UzimaHealth:contact")  # redirect back to contact page

    return render(request, "contact.html")
  # Redirects to login if not authenticated


def booking_page(request):
    if request.method == "POST":
        patient_name = request.POST["patient_name"]
        test_type = request.POST["test_type"]
        date = request.POST["date"]
        time = request.POST["time"]

        # Check for duplicate
        if Bookings.objects.filter(patient_name=patient_name, test_type=test_type, date=date, time=time).exists():
            messages.error(
                request,
                "Duplicate booking detected: This patient already has this test booked at the same date and time."
            )
            return render(request, "booking.html")

        try:
            booking = Bookings(
                patient_name=patient_name,
                age=request.POST["age"],
                contact_number=request.POST["contact_number"],
                test_type=test_type,
                date=date,
                time=time,
                hospital_name=request.POST["hospital_name"],
            )
            booking.save()  # booking_ref auto-generated

            # Render confirmation slip
            return render(request, "booking_confirmation.html", {
                "patient_name": booking.patient_name,
                "test_type": booking.get_test_type_display(),
                "date": booking.date,
                "time": booking.time,
                "hospital_name": booking.get_hospital_name_display(),
                "booking_ref": booking.booking_ref,
            })

        except IntegrityError:
            messages.error(request, "An error occurred while booking. Please try again.")
            return render(request, "booking.html")

    return render(request, "booking.html")


        # Render the booking page template


@login_required
def show_booking_page(request):
    query = request.GET.get("q", "")
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to view this page.")
        return redirect('UzimaHealth:Home')
    bookings = Bookings.objects.all()
    if query:
        bookings = bookings.filter(
            patient_name__icontains=query
        ) | bookings.filter(
            test_type__icontains=query
        )
    context = {'bookings': bookings, 'query': query}
    return render(request, 'show_booking.html', context)


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Bookings, id=booking_id)

    # Only admin/staff can delete
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not allowed to delete this booking.")
        return redirect('UzimaHealth:show_booking')
    booking.delete()
    messages.success(request, "Booking deleted successfully.")
    return redirect('UzimaHealth:show_booking')


@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(Bookings, id=booking_id)

    # Only admin/staff can edit
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not allowed to edit this booking.")
        return redirect('UzimaHealth:show_booking')

    if request.method == "POST":
        booking.patient_name = request.POST["patient_name"]
        booking.age = request.POST["age"]
        booking.contact_number = request.POST["contact_number"]
        booking.test_type = request.POST["test_type"]
        booking.date = request.POST["date"]
        booking.time = request.POST["time"]
        booking.hospital_name = request.POST["hospital_name"]
        booking.save()
        messages.success(request, "Booking updated successfully.")
        return redirect('UzimaHealth:show_booking')

    context = {'booking': booking}
    return render(request, 'update_booking.html', context)
