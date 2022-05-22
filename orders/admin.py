from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "storage",
        "delivery_status",
        "billing_status",
        "total_paid",
    )
    list_editable = ("delivery_status",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("price", "quantity")
