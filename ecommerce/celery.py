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

app.conf.beat_schedule = {
    "send-customer-product": {
        "task": "accounts.tasks.send_product",
        "schedule": crontab(minute=0, hour=10, day_of_week=1),
    }
}

app.autodiscover_tasks()
