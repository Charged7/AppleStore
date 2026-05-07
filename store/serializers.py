from rest_framework import serializers
from .models import (
    Product, ProductImage,
    IPhoneSpec, IPadSpec, MacBookSpec, IMacSpec,
    AppleWatchSpec, AirPodsSpec, AppleKeyboardSpec, AppleMouseSpec,
)


# ───────────────────────────────────────────
# SPEC SERIALIZERS
# ───────────────────────────────────────────

class BaseSpecSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["id", "product"]

class IPhoneSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = IPhoneSpec

class IPadSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = IPadSpec

class MacBookSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = MacBookSpec

class IMacSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = IMacSpec

class AppleWatchSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = AppleWatchSpec

class AirPodsSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = AirPodsSpec

class AppleKeyboardSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = AppleKeyboardSpec

class AppleMouseSpecSerializer(BaseSpecSerializer):
    class Meta(BaseSpecSerializer.Meta):
        model = AppleMouseSpec


# ───────────────────────────────────────────
# ДОПОМІЖНІ СЕРІАЛІЗАТОРИ
# ───────────────────────────────────────────

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt", "is_main", "order"]


# ───────────────────────────────────────────
# ГОЛОВНИЙ СЕРІАЛІЗАТОР ПРОДУКТУ
# ───────────────────────────────────────────

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    specs = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "category", "name", "slug", "sku",
            "price", "old_price", "discount_percent",
            "stock", "is_active", "description",
            "images", "specs", "created_at", "updated_at",
        ]

    @staticmethod
    def get_specs(obj):
        if obj.category.slug == "iphone":
            return IPhoneSpecSerializer(obj.iphone_spec).data
        if obj.category.slug == "ipad":
            return IPadSpecSerializer(obj.ipad_spec).data
        if obj.category.slug == "macbook":
            return MacBookSpecSerializer(obj.macbook_spec).data
        if obj.category.slug == "imac":
            return IMacSpecSerializer(obj.imac_spec).data
        if obj.category.slug == "watch":
            return AppleWatchSpecSerializer(obj.watch_spec).data
        if obj.category.slug == "airpods":
            return AirPodsSpecSerializer(obj.airpods_spec).data
        if obj.category.slug == "keyboard":
            return AppleKeyboardSpecSerializer(obj.keyboard_spec).data
        if obj.category.slug == "mouse":
            return AppleMouseSpecSerializer(obj.mouse_spec).data
        return None


class ProductCreateSerializer(serializers.ModelSerializer):
    specs = serializers.JSONField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "category", "name", "sku", "price",
            "old_price", "stock", "description", "specs"
        ]

    def create(self, validated_data):
        specs_data = validated_data.pop("specs")
        product = Product.objects.create(**validated_data)

        if product.category.slug == "iphone":
            IPhoneSpec.objects.create(product=product, **specs_data)
        elif product.category.slug == "ipad":
            IPadSpec.objects.create(product=product, **specs_data)
        elif product.category.slug == "macbook":
            MacBookSpec.objects.create(product=product, **specs_data)
        elif product.category.slug == "imac":
            IMacSpec.objects.create(product=product, **specs_data)
        elif product.category.slug == "watch":
            AppleWatchSpec.objects.create(product=product, **specs_data)
        elif product.category.slug == "airpods":
            AirPodsSpec.objects.create(product=product, **specs_data)
        elif product.category.slug == "keyboard":
            AppleKeyboardSpec.objects.create(product=product, **specs_data)
        elif product.category.slug == "mouse":
            AppleMouseSpec.objects.create(product=product, **specs_data)

        return product
