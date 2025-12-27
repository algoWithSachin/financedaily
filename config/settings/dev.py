from .base import *
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = os.environ.get("DEBUG") == "True"

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

STATICFILES_DIRS = [BASE_DIR / "static"]


# =========================
# Session Settings for Dev
# =========================
SESSION_COOKIE_AGE = 3600*3  # 3 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # expire when browser closes
SESSION_COOKIE_SECURE = False  # no HTTPS needed locally
SESSION_COOKIE_HTTPONLY = True  # prevent JS access
SESSION_SAVE_EVERY_REQUEST = True  # refresh expiry on every request

# ---------------------------
# EMAIL CONFIG
# ---------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = True

FRONTEND_URL = "http://127.0.0.1:8000"
DEFAULT_FROM_EMAIL = f"Finance Daily <{EMAIL_HOST_USER}>"