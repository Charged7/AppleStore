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
    is_new_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "slug",
            "color",
            "storage",
            "price",
            "old_price",
            "stock",
            "is_new",
            "new_until",
            "is_new_active",
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


class ProductVariantCardSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    category = serializers.CharField(source="product.category", read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = serializers.SerializerMethodField()
    discount_percent = serializers.IntegerField(read_only=True)
    is_new_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "slug",
            "name",
            "product_name",
            "product_slug",
            "category",
            "color",
            "storage",
            "price",
            "old_price",
            "discount_percent",
            "stock",
            "is_new",
            "new_until",
            "is_new_active",
            "images",
            "attributes",
        ]

    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        return " ".join(
            part
            for part in [obj.product.name, obj.storage, obj.color]
            if part
        )

    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_attributes(self, obj):
        return {
            attribute.name: attribute.value
            for attribute in obj.attributes.all()
        }


class ProductVariantOptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    is_new_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "slug",
            "name",
            "color",
            "storage",
            "price",
            "old_price",
            "discount_percent",
            "stock",
            "is_new",
            "new_until",
            "is_new_active",
            "images",
        ]

    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        return " ".join(
            part
            for part in [obj.product.name, obj.storage, obj.color]
            if part
        )


class ProductVariantDetailSerializer(ProductVariantCardSerializer):
    available_variants = serializers.SerializerMethodField()

    class Meta(ProductVariantCardSerializer.Meta):
        fields = ProductVariantCardSerializer.Meta.fields + ["available_variants"]

    @extend_schema_field(ProductVariantOptionSerializer(many=True))
    def get_available_variants(self, obj):
        variants = (
            obj.product.variants
            .all()
            .prefetch_related("images")
            .order_by("storage", "color")
        )
        return ProductVariantOptionSerializer(
            variants,
            many=True,
            context=self.context,
        ).data
