from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from store.models import TimeStampedModel


class CustomerManager(BaseUserManager):
    def create_superuser(self, email, full_name, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be assigned to is_staff=True"))

        elif other_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must be assigned to is_superuser=True")
            )
        return self.create_user(email, full_name, password, **other_fields)

    def create_user(self, email, full_name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_("Email address"),
        help_text=_("Required"),
        max_length=64,
        unique=True,
    )

    full_name = models.CharField(verbose_name=_("Full Name"), max_length=128)
    phone = models.CharField(verbose_name=_("Phone Number"), max_length=16)
    is_active = models.BooleanField(verbose_name=_("Is active"), default=False)
    is_staff = models.BooleanField(verbose_name=_("Is staff"), default=False)
    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")


class Address(TimeStampedModel):
    customer = models.ForeignKey(
        Customer, verbose_name=_("Customer"), on_delete=models.CASCADE
    )
    country = CountryField(_("Country"))
    town_city = models.CharField(_("Town/City"), max_length=128)
    address_line = models.CharField(_("Address Line"), max_length=255)
    full_name = models.CharField(_("Full Name"), max_length=64)
    phone = models.CharField(_("Phone Number"), max_length=16)
    latitude = models.DecimalField(
        verbose_name=_("Latitude"),
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        verbose_name=_("Longitude"),
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    delivery_instructions = models.CharField(
        verbose_name=_("Delivery Instructions"), max_length=255
    )
    default = models.BooleanField(_("Default"), default=False)

    def __str__(self):
        return self.address_line

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
