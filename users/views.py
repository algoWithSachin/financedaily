from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST



# ==============================
# Signup view
# ==============================
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        # username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "username already taken. Please choose another one.")
            return redirect('signup')
        
        email = request.POST.get('email')
        # email check
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already taken. Please choose another one.")
            return redirect('signup')

        password = request.POST.get('password')

        # Create user-obj
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Your account has been created successfully. Please log in to continue.")
        return redirect('login')
  
    return render(request, 'users/signup.html')


# ==============================
# Login view
# ==============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
        login(request, user)
        return redirect('dashboard')

    return render(request, 'users/login.html')


# ==============================
# Logout view
# ==============================
@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect('login')

# ==============================
# Landing page view
# ==============================
def landing_view(request):
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'users/landing.html')

