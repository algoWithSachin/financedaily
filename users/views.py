from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
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
        user.save()

        # create profile obj
        profile = Profile.objects.create(
            user=user,
            is_verified = False
        )

        # generate auth-token
        email_verification_token = generate_email_verification_token(profile)


        # send email for verfication
        send_mail_for_registration(email, email_verification_token)
        return redirect('email_verification_sent')
    
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

        login(request, user)  # soft gate: session exists

        try:
            profile = Profile.objects.select_related('user').get(user=user)
        except Profile.DoesNotExist:
            # This should never happen if signup always creates a profile
            messages.error(request, "Profile not found. Contact support.")
            logout(request)
            return redirect('login')

        if not profile.is_verified:
            messages.info(
                request,
                "Your account is not verified. Please verify your email to continue."
            )
            return redirect('resend_verification_email')

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



def landing_view(request):
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'users/landing.html')

def email_verification_sent_view(request):
    return render(request, 'users/email_verification_sent.html')

# ==============================
# verify view
# ==============================
def verify_email_view(request, token):

    profile = Profile.objects.filter(
        email_verification_token=token
    ).first()

    if not profile:
        messages.error(request, "Invalid verification link.")
        return redirect('login')

    if profile.is_verified:
        messages.info(request, "Account already verified.")
        return redirect('login')

    if now() - profile.token_created_at > timedelta(hours=24):
        messages.error(request, "Verification link expired.")
        return redirect('resend_verification_email')

    # ✅ VERIFY
    profile.is_verified = True
    profile.email_verification_token = None
    profile.token_created_at = None
    profile.save()

    messages.success(request, "Your account has been verified.")
    return redirect('login')


# ==============================
# send mail fuction
# ==============================

def send_mail_for_registration(email, token):

    verification_url = f"{settings.FRONTEND_URL}/verify/{token}/"

    subject = "Verify your email address"

    message = (
        "Thanks for signing up.\n\n"
        "Please verify your email by clicking the link below:\n\n"
        f"{verification_url}\n\n"
        "This link will expire in 24 hours.\n"
        "If you did not create this account, you can ignore this email."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )

# ==============================
# resend verfication email
# ==============================
from django.utils.timezone import now
from datetime import timedelta

def resend_verification_email(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to continue.")
        return redirect('login')
    profile = Profile.objects.filter(user=request.user).first()

    if not profile:
        messages.error(request, "Profile not found.")
        return redirect('login')

    if profile.is_verified:
        messages.info(request, "Account already verified.")
        return redirect('login')

    if request.method == 'POST':

        if (
            profile.last_verification_email_sent
            and now() - profile.last_verification_email_sent < timedelta(minutes=5)
        ):
            remaining_time = timedelta(minutes=5) - (now() - profile.last_verification_email_sent)
            remaining_minutes = max(1, int(remaining_time.total_seconds() // 60))

            messages.error(
                request,
                f"We’ve already sent a verification email recently. "
                f"Please check your inbox or try again in {remaining_minutes} minute(s)")  
            
            return redirect('resend_verification_email')

        token = generate_email_verification_token(profile)
        send_mail_for_registration(request.user.email, token)

        profile.last_verification_email_sent = now()
        profile.save(update_fields=['last_verification_email_sent'])
        return redirect('email_verification_sent')

    return render(request, 'users/resend_verification_email.html')


# ==============================
# generate email verfication token
# ==============================
def generate_email_verification_token(profile):
    profile.email_verification_token = str(uuid.uuid4())
    profile.token_created_at = now()
    profile.save()
    return profile.email_verification_token
