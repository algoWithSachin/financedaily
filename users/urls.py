from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_view, name="landing"),
    path('signup/', views.signup_view, name="signup"),
    path('email-verification-sent/', views.email_verification_sent_view, name="email_verification_sent"),
    path('verify/<str:token>/', views.verify_email_view, name="verify_email_view"),
    path('resend-verification-email/', views.resend_verification_email, name="resend_verification_email"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),

]
