from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="store_home"),
    path(
        "<slug:slug>", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "shop/<slug:category_slug>/",
        views.CategoryListView.as_view(),
        name="category_list",
    ),
    path("search/", views.ProductSearchView.as_view(), name="search"),
    path(
        "check-coupon/", views.CheckCouponView.as_view(), name="check_coupon"
    ),
]
