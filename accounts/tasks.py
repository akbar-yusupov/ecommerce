from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from accounts.models import Customer
from store.models import Coupon, Product


@shared_task(bind=True)
def send_available_coupons(self):
    if Coupon.available.exists():
        subject = _("Active Coupons")
        customers_email = (
            Customer.objects.filter(is_active=True)
            .exclude(is_staff=True)
            .values_list("email", flat=True)
        )
        coupons = Coupon.available.all()
        html_message = render_to_string(
            "accounts/celery/coupon_email.html",
            {"coupons": coupons, "host": settings.HOST},
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=customers_email,
            html_message=html_message,
        )

        return _("Celery task successfully sent emails")
    else:
        return _("Celery task does not have available coupons")


@shared_task(bind=True)
def send_product(self):
    if Product.objects.exists():
        subject = _("The product with the best benefit")
        customers_email = (
            Customer.objects.filter(is_active=True)
            .exclude(is_staff=True)
            .values_list("email", flat=True)
        )
        product = Product.objects.order_by("discount_percentage").first()
        html_message = render_to_string(
            "accounts/celery/product_email.html",
            {"product": product, "host": settings.HOST},
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=customers_email,
            html_message=html_message,
        )

        return _("Celery periodic task successfully sent emails")
    else:
        return _("Celery periodic task does not have available products")
