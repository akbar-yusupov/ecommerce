from random import sample

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.views import View
from django.views.generic import DetailView, ListView

from orders.models import OrderItem

from .models import Category, Coupon, Product, ProductRating, ProductsOfTheDay


class ProductListView(View):
    template_name = "store/index.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)

        categories = list(Category.objects.filter(level=0))
        random_categories = sample(
            categories, 5 if len(categories) >= 5 else len(categories)
        )

        products_of_the_day = ProductsOfTheDay.objects.first()
        if products_of_the_day:
            products_of_the_day = products_of_the_day.products.all().annotate(
                final_price=ExpressionWrapper(
                    F("regular_price")
                    - F("regular_price") / 100 * F("discount_percentage"),
                    output_field=DecimalField(),
                ),
                rating_sum=Sum("rating__score"),
                rating_count=Count("rating"),
            )

        most_rated = (
            products.annotate(
                rating_sum=Sum("rating__score"), rating_count=Count("rating")
            )
            .annotate(avg_score=F("rating_sum") / F("rating_count"))
            .order_by("-avg_score")[:5]
            .annotate(
                final_price=F("regular_price")
                - F("regular_price") / 100 * F("discount_percentage")
            )
            .select_related("category")
            .prefetch_related("product_image")
        )

        most_purchased = (
            products.annotate(
                purchased_times=Count("order_items"),
                rating_sum=Sum("rating__score"),
                rating_count=Count("rating"),
            )
            .order_by("-purchased_times")[:5]
            .annotate(
                final_price=F("regular_price")
                - F("regular_price") / 100 * F("discount_percentage")
            )
            .select_related("category")
            .prefetch_related("product_image")
        )

        return render(
            request,
            self.template_name,
            {
                "random_categories": random_categories,
                "products_of_the_day": products_of_the_day,
                "most_rated": most_rated,
                "most_purchased": most_purchased,
            },
        )


class CategoryListView(ListView):
    model = Category
    template_name = "store/category.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        return (
            Product.objects.filter(
                category__in=Category.objects.get(
                    slug=self.kwargs["category_slug"]
                ).get_descendants(include_self=True)
            )
            .select_related("category")
            .prefetch_related("product_image")
            .annotate(
                final_price=F("regular_price")
                - F("regular_price") / 100 * F("discount_percentage")
            )
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category.objects.all().prefetch_related("products"),
            slug=self.kwargs["category_slug"],
        )
        context["category"] = category
        context["subcategories"] = category.get_descendants()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product.objects.all()
    template_name = "store/single.html"

    def __init__(self, *args, **kwargs):
        self.ratable = False
        self.user_stars = False
        super().__init__(*args, **kwargs)

    def get_object(self, queryset=None):
        product = get_object_or_404(
            self.model.prefetch_related("product_image", "specifications"),
            slug=self.kwargs["slug"],
            is_active=True,
        )
        product.final_price = product.regular_price - (
            product.regular_price / 100 * product.discount_percentage
        )
        product.purchased_times = OrderItem.objects.filter(
            product=product
        ).count()
        recently_viewed_products = None
        product_pk = product.pk

        if "recently_viewed" in self.request.session:
            if product_pk in self.request.session["recently_viewed"]:
                self.request.session["recently_viewed"].remove(product_pk)

            products = self.model.filter(
                pk__in=self.request.session["recently_viewed"]
            ).prefetch_related("product_image")
            recently_viewed_products = sorted(
                products,
                key=lambda x: self.request.session["recently_viewed"].index(
                    x.id
                ),
            )
            self.request.session["recently_viewed"].insert(0, product_pk)
            if len(self.request.session["recently_viewed"]) > 5:
                self.request.session["recently_viewed"].pop()
        else:
            self.request.session["recently_viewed"] = [product_pk]
        self.request.session.modified = True

        product.recently_viewed_products = recently_viewed_products

        product_ratings = product.rating.all()
        product_rating_customers__pk = product_ratings.values_list(
            "customer__pk", flat=True
        )
        if self.request.user.pk in product_rating_customers__pk:
            idx = list(product_rating_customers__pk).index(
                self.request.user.pk
            )
            product_rating = product_ratings[idx]
        else:
            product_rating = False
        product_bought = OrderItem.objects.filter(
            product=product, order__address__customer=self.request.user
        ).exists()
        if product_rating:
            self.user_stars = range(product_rating.score)
        elif product_bought:
            self.ratable = True
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ratable"] = self.ratable
        context["user_stars"] = self.user_stars
        return context

    def post(self, request, *args, **kwargs):
        try:
            stars = int(request.POST["stars"])
            if not (1 <= stars <= 5):
                raise BadRequest("Stars should be between 1 and 5")
        except ValueError:
            raise BadRequest("Stars should be integer")
        product = self.get_object()
        if self.ratable:
            ProductRating.objects.create(
                product=product, customer=request.user, score=stars
            )
        messages.info(
            request,
            f"You have successfully rated the product to {str(stars)} stars",
        )
        return redirect("store:product_detail", self.kwargs["slug"])


class ProductSearchView(ListView):
    model = Product.objects.all()
    template_name = "store/search.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        products = self.model
        search = self.request.GET.get("q", None)

        if search:
            if translation.get_language() == "ru":
                print("ru")
                products = self.model.filter(
                    title_ru__icontains=search
                ).distinct()
            elif translation.get_language() == "en":
                print("en")
                products = self.model.filter(
                    title_en__icontains=search
                ).distinct()
        return (
            products.select_related("category")
            .prefetch_related("product_image")
            .annotate(
                final_price=F("regular_price")
                - F("regular_price") / 100 * F("discount_percentage")
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.get_queryset())
        context["products_number"] = self.get_queryset().count()
        return context


class CheckCouponView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        coupon_code = request.POST["coupon_code"]
        coupon = Coupon.available.filter(code=coupon_code).first()
        if coupon:
            request.session["coupon_discount"] = coupon.discount
            request.session.modified = True
            return JsonResponse({"coupon_discount": coupon.discount})
        else:
            request.session["coupon_discount"] = 0
            request.session.modified = True
            return JsonResponse({"coupon_discount": 0})
