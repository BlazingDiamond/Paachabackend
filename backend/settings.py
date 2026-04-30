"""
Django settings for backend project.
"""

import importlib.util
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#)%l!i003%ov6q#m!fpjb5u665fcl+$o^^=un2#d!rd+!%v57g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# Application definition

INSTALLED_APPS = []

# Prefer a modern business dashboard if available.
if importlib.util.find_spec("unfold"):
    INSTALLED_APPS.append("unfold")
elif importlib.util.find_spec("jazzmin"):
    INSTALLED_APPS.append("jazzmin")
if importlib.util.find_spec("appointment"):
    INSTALLED_APPS.append("appointment")

INSTALLED_APPS += [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "tours",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", ""),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Johannesburg"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Admin branding
ADMIN_SITE_HEADER = "Paacha Admin Gateway"
ADMIN_SITE_TITLE = "Paacha Control Panel"
ADMIN_INDEX_TITLE = "Tour Operations Dashboard"

# Optional Django Unfold configuration
UNFOLD = {
    "SITE_TITLE": ADMIN_SITE_TITLE,
    "SITE_HEADER": ADMIN_SITE_HEADER,
    "SITE_SUBHEADER": "Client Control Panel",
    "SHOW_HISTORY": True,
}

# Local payment gateways (configure credentials in env vars)
PAYMENT_PROVIDERS = {
    "PAYFAST": {
        "MERCHANT_ID": os.getenv("PAYFAST_MERCHANT_ID", ""),
        "MERCHANT_KEY": os.getenv("PAYFAST_MERCHANT_KEY", ""),
        "PASSPHRASE": os.getenv("PAYFAST_PASSPHRASE", ""),
        "SANDBOX": os.getenv("PAYFAST_SANDBOX", "True").lower() == "true",
    },
    "PEACH_PAYMENTS": {
        "ENTITY_ID": os.getenv("PEACH_ENTITY_ID", ""),
        "ACCESS_TOKEN": os.getenv("PEACH_ACCESS_TOKEN", ""),
        "BASE_URL": os.getenv("PEACH_BASE_URL", ""),
    },
    "YOCO": {
        "PUBLIC_KEY": os.getenv("YOCO_PUBLIC_KEY", ""),
        "SECRET_KEY": os.getenv("YOCO_SECRET_KEY", ""),
    },
}
