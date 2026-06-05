from django.urls import path
from .views import landing_view, signup_view, login_view, logout_view


urlpatterns = [
    path('', landing_view, name="landing"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name='logout'),
]
