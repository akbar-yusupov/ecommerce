from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Coupon,
    Product,
    ProductImage,
    ProductRating,
    ProductsOfTheDay,
    ProductSpecifications,
    Storage,
)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "valid_from",
        "valid_to",
        "discount",
        "is_active",
    )
    list_filter = ("is_active",)
    list_editable = ("code", "is_active", "discount")


class ProductSpecificationsInline(TranslationTabularInline):
    model = ProductSpecifications


class ProductImageInline(TranslationTabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ("title", "description", "slug", "is_active")
    list_editable = ("is_active",)
    list_filter = ("category",)
    search_fields = ("title", "description")
    inlines = (ProductImageInline, ProductSpecificationsInline)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("users_wishlist",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.readonly_fields = ("created_at", "updated_at")
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ("product", "score")


@admin.register(ProductsOfTheDay)
class ProductsOfTheDayAdmin(admin.ModelAdmin):
    filter_horizontal = ("products",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.readonly_fields = ("updated_at",)
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Storage)
class StorageAdmin(TranslationAdmin):
    list_display = ("name", "city")
    search_fields = ("name", "city")


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_editable = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
