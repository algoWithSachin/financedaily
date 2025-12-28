from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["financedaily.onrender.com"]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
    )
}

STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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

