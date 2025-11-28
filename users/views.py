from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# ==============================
# Signup view
# ==============================
def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Password check
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            password=password1
        )
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')
    
    return render(request, 'users/signup.html')


# ==============================
# Login view
# ==============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "User not found. Please sign up first.")
            return redirect('login')

        # Authenticate credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # session will use settings.py defaults
            messages.success(request, f"Welcome back, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect password. Try again.")
            return redirect('login')

    return render(request, 'users/login.html')


# ==============================
# Logout view
# ==============================
def logout_view(request):
    logout(request)  # clears session and authentication
    messages.success(request, "You have been logged out.")
    return redirect('login')


def landing_view(request):
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'users/landing.html')