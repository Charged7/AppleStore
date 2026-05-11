from rest_framework import serializers
from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from .models import Product, ProductVariant, ProductAttribute, ProductImage


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


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name", "value"]


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


class ProductVariantCreateSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, required=False)

    class Meta:
        model = ProductVariant
        fields = [
            "color",
            "storage",
            "price",
            "old_price",
            "stock",
            "attributes",
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    variants = ProductVariantCreateSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["category", "name", "description", "is_active", "variants"]

    @transaction.atomic
    def create(self, validated_data):
        variants_data = validated_data.pop("variants", [])
        product = Product.objects.create(**validated_data)

        for variant_data in variants_data:
            attributes_data = variant_data.pop("attributes", [])
            variant = ProductVariant.objects.create(
                product=product,
                **variant_data,
            )
            ProductAttribute.objects.bulk_create([
                ProductAttribute(variant=variant, **attribute_data)
                for attribute_data in attributes_data
            ])

        return product

    def to_representation(self, instance):
        return ProductSerializer(instance, context=self.context).data
