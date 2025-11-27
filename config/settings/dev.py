from .base import *
import os

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
]

# Force sqlite in dev
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================
# Session Settings for Dev
# =========================
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # expire when browser closes
SESSION_COOKIE_SECURE = False  # no HTTPS needed locally
SESSION_COOKIE_HTTPONLY = True  # prevent JS access
SESSION_SAVE_EVERY_REQUEST = True  # refresh expiry on every request
