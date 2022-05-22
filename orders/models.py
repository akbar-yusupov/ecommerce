from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Address
from store.models import Product, Storage, TimeStampedModel


class Order(TimeStampedModel):
    class DeliveryChoices(models.IntegerChoices):
        not_out_yet = 1, _("Not out yet")
        on_the_way = 2, _("On the way")
        delivered = 3, _("Delivered")

    address = models.ForeignKey(
        Address, verbose_name=_("Address"), on_delete=models.CASCADE
    )
    storage = models.ForeignKey(
        Storage, verbose_name=_("Storage"), on_delete=models.CASCADE
    )
    total_paid = models.DecimalField(
        verbose_name=_("Total paid"), max_digits=12, decimal_places=2
    )
    order_key = models.CharField(verbose_name=_("Order key"), max_length=128)
    billing_status = models.BooleanField(
        verbose_name=_("Billing status"), default=False
    )
    delivery_status = models.PositiveSmallIntegerField(
        verbose_name=_("Delivery status"),
        choices=DeliveryChoices.choices,
        default=1,
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=12, decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=1
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")
