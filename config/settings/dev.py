from .base import *
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'financedaily',
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASS"),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = BASE_DIR / "staticfiles"

# =========================
# Session Settings for Dev
# =========================
SESSION_COOKIE_AGE = 3600 * 3
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # expire when browser closes
SESSION_COOKIE_SECURE = False  # no HTTPS needed locally
SESSION_COOKIE_HTTPONLY = True  # prevent JS access
SESSION_SAVE_EVERY_REQUEST = True  # refresh expiry on every request



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}




# 1. Existing INSTALLED_APPS mein toolbar append karo
INSTALLED_APPS += [
    "debug_toolbar",
]

# 2. MIDDLEWARE mein toolbar ka middleware add karo
# Note: Isko hamesha baaki middlewares ke upar ya bilkul shuruat mein rakhna chahiye
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

# 3. Yeh batana zaroori hai, iske bina toolbar browser mein nahi dikhega
INTERNAL_IPS = [
    "127.0.0.1",
]
