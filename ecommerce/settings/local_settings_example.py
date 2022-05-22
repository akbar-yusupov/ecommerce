HOST = "http://127.0.0.1:8000"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecommerce",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST_USER = "admin@admin.com"
EMAIL_HOST = ""
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = ""

STRIPE_PUBLISHABLE_KEY = ""
STRIPE_SECRET_KEY = ""
STRIPE_ENDPOINT_SECRET = ""
# stripe listen --forward-to localhost:8000/payment/webhook/
