from datetime import datetime

import pytest
from pytest_factoryboy import register

from tests.factories import (
    AddressFactory,
    CategoryFactory,
    CouponFactory,
    CustomerFactory,
    ProductFactory,
    ProductRatingFactory,
    ProductSpecificationsFactory,
    StorageFactory,
    ProductsOfTheDayFactory
)

register(CustomerFactory)
register(AddressFactory)

register(CategoryFactory)
register(ProductFactory)
register(ProductRatingFactory)
register(CustomerFactory)
register(ProductSpecificationsFactory)
register(CouponFactory)
register(StorageFactory)
register(ProductsOfTheDayFactory)


# Accounts
@pytest.fixture
def customer(db, customer_factory):
    new_customer = customer_factory.create()
    return new_customer


@pytest.fixture
def admin_customer(db, customer_factory):
    new_customer = customer_factory.create(
        email="new_admin@email.com",
        full_name="new_admin",
        is_staff=True,
        is_superuser=True,
    )
    return new_customer


@pytest.fixture
def address(db, address_factory):
    address = address_factory.create()
    return address


# Store
@pytest.fixture
def product_category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()
    return product


@pytest.fixture
def product_rating(db, product_rating_factory):
    product_rating = product_rating_factory.create()
    return product_rating


@pytest.fixture
def product_specifications(db, product_specifications_factory):
    product_specification = product_specifications_factory.create()
    return product_specification


@pytest.fixture
def coupon(db, coupon_factory):
    coupon = coupon_factory.create()
    return coupon


@pytest.fixture
def storage(db, storage_factory):
    storage = storage_factory.create()
    return storage


@pytest.fixture
def products_of_the_day(db, products_of_the_day_factory):
    products_of_the_day = products_of_the_day_factory.create()
    products_of_the_day.save()
    return products_of_the_day
