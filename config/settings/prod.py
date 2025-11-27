from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]  # MUST be set

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
    )
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =========================
# Session Settings 
# =========================
SESSION_COOKIE_AGE = 172800  # 48 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # prod shouldn't auto-expire on close
SESSION_COOKIE_SECURE = True  # force HTTPS only
SESSION_COOKIE_HTTPONLY = True  # JS can't touch the cookie
SESSION_COOKIE_SAMESITE = "Lax"  # or 'Strict' if you don't need cross-site
SESSION_SAVE_EVERY_REQUEST = False  # no sliding window; use fixed timeout