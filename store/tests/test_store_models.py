import pytest
from django.urls import reverse

from tests.factories import CouponFactory


def test_category_str(product_category):
    assert str(product_category) == "django"


def test_category_reverse(client, product_category):
    url = reverse("store:category_list", args=(product_category.slug,))
    response = client.get(url)
    assert response.status_code == 200


def test_product_str(product):
    assert str(product) == "pc"


def test_product_reverse(client, product, customer):
    # url = reverse("store:product_detail", args=(product.slug, ))
    url = product.get_absolute_url()
    client.force_login(customer)
    response = client.get(url)
    assert response.status_code == 200


def test_product_active_image(product):
    assert product.active_image()


def test_product_rating_str(product_rating):
    assert str(product_rating) == "4"


def test_product_specifications_str(product_specifications):
    assert str(product_specifications) == "Processor"


def test_coupon_str(coupon):
    assert str(coupon) == "Xq2fsB3fwqA"


# def test_coupon_manager(coupon):
#     CouponFactory.create(code="a3sWd1qAS")
#     assert CouponFactory.available()


def test_storage_str(storage):
    assert str(storage) == "Tashkent, Main"


def test_products_of_the_day_str(products_of_the_day):
    assert str(products_of_the_day) != products_of_the_day.updated_at
