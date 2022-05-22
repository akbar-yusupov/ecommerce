from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from mptt.models import MPTTModel, TreeForeignKey


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("Created at"), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True
    )

    class Meta:
        abstract = True


class Category(MPTTModel):
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="categories/",
        help_text=_("Required"),
    )
    slug = models.SlugField(
        verbose_name=_("Category URL"), max_length=255, unique=True
    )
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.RESTRICT,
        related_name="products",
    )
    title = models.CharField(
        verbose_name=_("Title"), help_text=_("Required"), max_length=255
    )
    description = models.TextField(
        verbose_name=_("Description"), help_text=_("Not required"), blank=True
    )
    slug = models.SlugField(
        verbose_name=_("Product URL"), help_text=_("Required"), max_length=255
    )
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 9999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999.99"),
            }
        },
        max_digits=6,
        decimal_places=2,
    )
    discount_percentage = models.IntegerField(
        verbose_name=_("Discount percentage"),
        help_text=_("Maximum 99%"),
        error_messages={
            "name": {
                "max_length": _("Percentage between 0 and 99"),
            }
        },
        validators=[MinValueValidator(0), MaxValueValidator(99)],
    )
    users_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Users wishlist"),
        related_name="user_wishlist",
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def active_image(self):
        return self.product_image.all().filter(is_featured=True).first()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_price_constraint",
                check=models.Q(
                    regular_price__gt=0,
                ),
            ),
        ]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductRating(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        related_name="rating",
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Customer"),
        on_delete=models.CASCADE,
    )

    score = models.SmallIntegerField(
        verbose_name=_("Score"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    def __str__(self):
        return str(self.score)

    class Meta:
        verbose_name = _("Product Rating")
        verbose_name_plural = _("Product Ratings")


class ProductSpecifications(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        related_name="specifications",
        on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    value = models.CharField(verbose_name=_("Value"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="product_image",
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to="products/%Y/%m/%d",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please enter alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_featured = models.BooleanField(
        verbose_name=_("Is Featured"),
        help_text=_("Main image checkbox"),
        default=False,
    )

    def save(self, *args, **kwargs):
        is_featured_query = ProductImage.objects.filter(
            product=self.product, is_featured=True
        ).exists()
        if is_featured_query:
            raise ValidationError(_("You need a featured image"))
        elif self.is_featured:
            if is_featured_query:
                raise ValidationError(
                    f"{self.product.title}"
                    + _(" can have only 1 featured image(for main pages)")
                )
        else:
            if not ProductImage.objects.filter(
                product=self.product, is_featured=True
            ).exists():
                self.is_featured = True
                self.save()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if not ProductImage.objects.filter(product=self.product).count() > 1:
            raise ValidationError(_("You cannot delete all product's images"))
        else:
            super().delete(using, keep_parents)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


class ProductsOfTheDay(models.Model):
    """
    Singleton Model
    """

    products = models.ManyToManyField(
        Product,
        verbose_name=_("Products list"),
        help_text=_("Only first 5 products will be shown"),
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True
    )

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        verbose_name = _("Product of the day")
        verbose_name_plural = _("Products of the day")


class CouponManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now(),
            )
        )


class Coupon(models.Model):
    code = models.CharField(verbose_name=_("Code"), max_length=64, unique=True)
    valid_from = models.DateTimeField(verbose_name=_("Valid from"))
    valid_to = models.DateTimeField(verbose_name=_("Valid to"))
    discount = models.IntegerField(
        verbose_name=_("Discount"),
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)
    objects = models.Manager()
    available = CouponManager()

    def __str__(self):
        return self.code


class Storage(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    country = CountryField(_("Country"))
    city = models.CharField(verbose_name=_("City"), max_length=64)
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

    def __str__(self):
        return f"{self.city}, {self.name}"

    class Meta:
        verbose_name = _("Storage")
        verbose_name_plural = _("Storages")
