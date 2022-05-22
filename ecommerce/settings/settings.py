import os
from pathlib import Path

from .local_settings import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = (
    "django-insecure-+tc^li88%5&z@3^&2sa-t)1(lfpvkq-1$kd*l)0k9naad2a3kj"
)

DEBUG = True

ALLOWED_HOSTS = ["store.com", "127.0.0.1", "*"]

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "mptt",
    "django_countries",
    "django_celery_results",
    "django_celery_beat",
    # my apps
    "store",
    "basket",
    "accounts",
    "payment",
    "orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.categories",
                "basket.context_processors.basket",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "en"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

BASKET_SESSION_ID = "basket"

AUTH_USER_MODEL = "accounts.Customer"
LOGIN_URL = "accounts:register"
LOGIN_REDIRECT_URL = "accounts:dashboard"

gettext = lambda s: s
LANGUAGES = (("en", gettext("English")), ("ru", gettext("Russian")))

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"),)

GEOIP_PATH = os.path.join(BASE_DIR, "geoip")

# CELERY SETTINGS
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Tashkent"
CELERY_RESULT_BACKEND = "django-db"

# CELERY BEAT
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
