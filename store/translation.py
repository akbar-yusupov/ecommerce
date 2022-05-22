from modeltranslation.translator import TranslationOptions, register

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecifications,
    Storage,
)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(ProductImage)
class ProductImageTranslationOptions(TranslationOptions):
    fields = ("alt_text",)


@register(ProductSpecifications)
class ProductSpecificationsTranslationOptions(TranslationOptions):
    fields = ("name", "value")


@register(Storage)
class StorageTranslationOptions(TranslationOptions):
    fields = ("name", "city")
