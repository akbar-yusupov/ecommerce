# Generated by Django 3.2.13 on 2022-05-22 12:16

import django.core.validators
import django.db.models.deletion
import django_countries.fields
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Required and unique",
                        max_length=255,
                        unique=True,
                        verbose_name="Category Name",
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        help_text="Required and unique",
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Category Name",
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        help_text="Required and unique",
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Category Name",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Required",
                        upload_to="categories/",
                        verbose_name="Image",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=255,
                        unique=True,
                        verbose_name="Category URL",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Is active"
                    ),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                (
                    "tree_id",
                    models.PositiveIntegerField(db_index=True, editable=False),
                ),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="store.category",
                        verbose_name="Parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=64, unique=True, verbose_name="Code"
                    ),
                ),
                (
                    "valid_from",
                    models.DateTimeField(verbose_name="Valid from"),
                ),
                ("valid_to", models.DateTimeField(verbose_name="Valid to")),
                (
                    "discount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(99),
                        ],
                        verbose_name="Discount",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Is active"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created at"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Updated at"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Required",
                        max_length=255,
                        verbose_name="Title",
                    ),
                ),
                (
                    "title_en",
                    models.CharField(
                        help_text="Required",
                        max_length=255,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "title_ru",
                    models.CharField(
                        help_text="Required",
                        max_length=255,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Not required",
                        verbose_name="Description",
                    ),
                ),
                (
                    "description_en",
                    models.TextField(
                        blank=True,
                        help_text="Not required",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "description_ru",
                    models.TextField(
                        blank=True,
                        help_text="Not required",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Required",
                        max_length=255,
                        verbose_name="Product URL",
                    ),
                ),
                (
                    "regular_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={
                            "name": {
                                "max_length": "The price must be between 0 and 9999.99"
                            }
                        },
                        help_text="Maximum 9999.99",
                        max_digits=6,
                        verbose_name="Regular price",
                    ),
                ),
                (
                    "discount_percentage",
                    models.IntegerField(
                        error_messages={
                            "name": {
                                "max_length": "Percentage between 0 and 99"
                            }
                        },
                        help_text="Maximum 99%",
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(99),
                        ],
                        verbose_name="Discount percentage",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Change product visibility",
                        verbose_name="Product visibility",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="products",
                        to="store.category",
                        verbose_name="Category",
                    ),
                ),
                (
                    "users_wishlist",
                    models.ManyToManyField(
                        blank=True,
                        related_name="user_wishlist",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users wishlist",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="Storage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Name"),
                ),
                (
                    "name_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        max_length=2, verbose_name="Country"
                    ),
                ),
                ("city", models.CharField(max_length=64, verbose_name="City")),
                (
                    "city_en",
                    models.CharField(
                        max_length=64, null=True, verbose_name="City"
                    ),
                ),
                (
                    "city_ru",
                    models.CharField(
                        max_length=64, null=True, verbose_name="City"
                    ),
                ),
                (
                    "latitude",
                    models.DecimalField(
                        decimal_places=4,
                        max_digits=6,
                        validators=[
                            django.core.validators.MinValueValidator(-90),
                            django.core.validators.MaxValueValidator(90),
                        ],
                        verbose_name="Latitude",
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        decimal_places=4,
                        max_digits=6,
                        validators=[
                            django.core.validators.MinValueValidator(-90),
                            django.core.validators.MaxValueValidator(90),
                        ],
                        verbose_name="Longitude",
                    ),
                ),
            ],
            options={
                "verbose_name": "Storage",
                "verbose_name_plural": "Storages",
            },
        ),
        migrations.CreateModel(
            name="ProductSpecifications",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Name"),
                ),
                (
                    "name_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "value",
                    models.CharField(max_length=255, verbose_name="Value"),
                ),
                (
                    "value_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Value"
                    ),
                ),
                (
                    "value_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Value"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specifications",
                        to="store.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Specification",
                "verbose_name_plural": "Product Specifications",
            },
        ),
        migrations.CreateModel(
            name="ProductsOfTheDay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Updated at"
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        help_text="Only first 5 products will be shown",
                        to="store.Product",
                        verbose_name="Products list",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product of the day",
                "verbose_name_plural": "Products of the day",
            },
        ),
        migrations.CreateModel(
            name="ProductRating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="Score",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Customer",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating",
                        to="store.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Rating",
                "verbose_name_plural": "Product Ratings",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created at"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Updated at"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="images/default.png",
                        help_text="Upload a product image",
                        upload_to="products/%Y/%m/%d",
                        verbose_name="Image",
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(
                        blank=True,
                        help_text="Please enter alternative text",
                        max_length=255,
                        null=True,
                        verbose_name="Alternative text",
                    ),
                ),
                (
                    "alt_text_en",
                    models.CharField(
                        blank=True,
                        help_text="Please enter alternative text",
                        max_length=255,
                        null=True,
                        verbose_name="Alternative text",
                    ),
                ),
                (
                    "alt_text_ru",
                    models.CharField(
                        blank=True,
                        help_text="Please enter alternative text",
                        max_length=255,
                        null=True,
                        verbose_name="Alternative text",
                    ),
                ),
                (
                    "is_featured",
                    models.BooleanField(
                        default=False,
                        help_text="Main image checkbox",
                        verbose_name="Is Featured",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_image",
                        to="store.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Image",
                "verbose_name_plural": "Product Images",
            },
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                check=models.Q(("regular_price__gt", 0)),
                name="store_product_price_constraint",
            ),
        ),
    ]