from datetime import datetime

import factory
from django.core.files.base import ContentFile
from faker import Faker

from accounts.models import Address, Customer
from store.models import (
    Category,
    Coupon,
    Product,
    ProductImage,
    ProductRating,
    ProductSpecifications,
    Storage, ProductsOfTheDay,
)

fake = Faker()


# Accounts
class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    email = "admin@admin.com"
    full_name = "First Admin"
    phone = "+99899 123 45 67"
    password = "admin"
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(CustomerFactory)
    address_line = "my address line"
    latitude = 45
    longitude = 45


# Store
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "django"
    slug = "django"


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(
        CategoryFactory, name="django", slug="django"
    )
    title = "pc"
    regular_price = 123
    discount_percentage = 3
    slug = "my_pc"
    product_image = factory.RelatedFactory(
        ProductImageFactory,
        factory_related_name="product",
        image=factory.LazyAttribute(
            lambda _: ContentFile(
                factory.django.ImageField()._make_data(
                    {"width": 1024, "height": 768}
                ),
                "example.jpg",
            )
        ),
        is_featured=True,
    )


class ProductRatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductRating

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerFactory)
    score = 4


class ProductSpecificationsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecifications

    product = factory.SubFactory(ProductFactory)
    name = "Processor"
    value = fake.text(max_nb_chars=16)


class CouponFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coupon

    code = "Xq2fsB3fwqA"
    valid_from = fake.date()
    valid_to = fake.date()
    discount = 3
    is_active = True


class StorageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Storage

    name = "Main"
    city = "Tashkent"
    latitude = 43.4
    longitude = 32.5


class ProductsOfTheDayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductsOfTheDay

    products = factory.RelatedFactory(ProductFactory)

