from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Product, ProductVariant, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "alt",
            "is_main",
            "order"
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = serializers.SerializerMethodField()
    discount_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "color",
            "storage",
            "price",
            "old_price",
            "stock",
            "discount_percent",
            "images",
            "attributes",
        ]

    # API повертає чистіший вигляд
    # attributes": { "chip": "A19 Pro", "ram": "8GB" }
    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_attributes(self, obj):
        return {
            attribute.name: attribute.value
            for attribute in obj.attributes.all()
        }


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "variants",
        ]
