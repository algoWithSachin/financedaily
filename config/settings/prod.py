from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [h for h in os.environ["DJANGO_ALLOWED_HOSTS"].split(",") if h]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
    )
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# =========================
# Session Settings 
# =========================
SESSION_COOKIE_AGE = 172800  
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  
SESSION_COOKIE_SECURE = True  
SESSION_COOKIE_HTTPONLY = True 
SESSION_COOKIE_SAMESITE = "Lax"  
SESSION_SAVE_EVERY_REQUEST = False  

# ---------------------------
# EMAIL CONFIG
# ---------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"].lower() in ("true", "1", "yes")
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
FRONTEND_URL = os.environ["FRONTEND_URL"]


CSRF_TRUSTED_ORIGINS = [FRONTEND_URL]
