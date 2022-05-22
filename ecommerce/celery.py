from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "ecommerce.settings.development_settings"
)

app = Celery("ecommerce")
app.conf.enable_utc = False

app.conf.update(timezone="Asia/Tashkent")

app.config_from_object(settings, namespace="CELERY")

# Periodic task - раз в неделю всем отправлять продукт с самой большой скидкой

app.conf.beat_schedule = {
    "send-customer-product": {
        "task": "accounts.tasks.send_product",
        "schedule": crontab(hour=11, minute=55),
    }
}

app.autodiscover_tasks()
