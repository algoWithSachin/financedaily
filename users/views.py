from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect('signup')


        # If all good — create the user
        user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, password=password1)
        user.save()
        # messages.success(request, "Account created successfully. Please log in.")
        # print(username, firstname,lastname, password1, password2) 
        return redirect('login')
    
    
    return render(request, 'users/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 1. Check if username exists in the database
        if not User.objects.filter(username=username).exists():
            messages.error(request, "User not found. Please sign up first.")
            return redirect('login')

        # 2. If user exists, check password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, f"Welcome back, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect password. Try again.")
            return redirect('login')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)  # removes the user’s session
    return redirect('login')  # or wherever you want them to go next
