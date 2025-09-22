from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden


# User Registration
def register_view(request):
    # Registration is disabled. Redirect to login with message.
    messages.error(request, 'Registration is disabled. Only admin users can log in.')
    return redirect('accounts:login')


# User Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not (user.is_staff or user.is_superuser):
                messages.error(request, "Only admin users can log in.")
                return redirect('accounts:login')
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('UzimaHealth:show_booking')  # redirect to booking page after login
            else:
                messages.error(request, "Your account is disabled. Please contact support.")
        else:
            messages.error(request, "Invalid username or password")

        return redirect('accounts:login')

    return render(request, 'accounts/login.html')

# User Logout
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('UzimaHealth:Home')  # Redirect to Home after logout
    return HttpResponseForbidden("Forbidden: This URL only accepts POST requests.")
