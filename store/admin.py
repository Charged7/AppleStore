from django.contrib import admin
from .models import (
    Product,
    ProductVariant,
    ProductAttribute,
    ProductImage,
)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ("color", "storage", "price", "old_price", "stock", "is_new", "new_until")


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ("name", "value")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt", "is_main", "order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "slug",
        "color",
        "storage",
        "price",
        "stock",
        "is_new",
        "new_until",
    )
    list_filter = ("product__category", "storage", "color", "is_new")
    search_fields = ("product__name", "slug", "color", "storage")
    readonly_fields = ("slug",)
    inlines = [ProductAttributeInline, ProductImageInline]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ("variant", "name", "value")
    list_filter = ("name",)
    search_fields = ("variant__product__name", "name", "value")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("variant", "alt", "is_main", "order")
    list_filter = ("is_main",)
    search_fields = ("variant__product__name", "alt")
