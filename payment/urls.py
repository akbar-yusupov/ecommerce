from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path("", views.PaymentView.as_view(), name="basket"),
    path(
        "order-placed/", views.OrderPlacedView.as_view(), name="order_placed"
    ),
    path("webhook/", views.stripe_webhook, name="webhook"),
]
