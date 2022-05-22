from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product

User = get_user_model()


class TestCategoryModel(TestCase):
    def setUp(self):
        self.new_category = Category.objects.create(
            name="django", slug="django"
        )

    def test_category_model(self):
        """
        Test store.models.Category().__str__()
        """
        data = self.new_category
        self.assertTrue(str(data), "django")


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name="django", slug="django")
        User.objects.create(username="admin")
        self.new_product = Product.objects.create(
            category_id=1,
            title="django by example",
            created_by_id=1,
            slug="django-by-example",
            price="20.00",
            image="django",
        )

    def test_product_model(self):
        """
        Test store.models.Product().__str__()
        """
        data = self.new_product
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "django by example")


class TestViewResponses(TestCase):
    def setUp(self):
        self.client_ = Client()
        self.factory = RequestFactory()

        User.objects.create(username="admin")
        Category.objects.create(name="django", slug="django")
        Product.objects.create(
            category_id=1,
            title="django book",
            created_by_id=1,
            slug="django-book",
            price="122223.42",
            image="django",
        )

    def test_url_allowed_hosts(self):
        response = self.client_.get("`", HTTP_HOST="wrongaddress.com")
        self.assertEqual(response.status_code, 404)
        response = self.client_.get("", HTTP_HOST="store.com")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.client_.get(
            reverse("store:product_detail", args=["django-book"])
        )
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        response = self.client_.get(
            reverse("store:category_list", args=["django"])
        )
        self.assertEqual(response.status_code, 200)
