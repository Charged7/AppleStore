from django.db.models import Min, Q, Sum
from django.utils import timezone
from django_filters import rest_framework as django_filters
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters
from rest_framework import viewsets
from .models import Product, ProductVariant
from .serializers import (
    ProductSerializer,
    ProductVariantCardSerializer,
    ProductVariantDetailSerializer,
)


ATTRIBUTE_FILTER_PARAMETERS = [
    OpenApiParameter(
        name="model",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="Filter by product model name. Example: iPhone 15 Pro.",
    ),
    OpenApiParameter(
        name="ram",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="Filter by RAM attribute. Example: 8GB.",
    ),
    OpenApiParameter(
        name="sim",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="Filter by SIM attribute. Example: eSIM.",
    ),
    OpenApiParameter(
        name="attr_chip",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="Example dynamic attribute filter. Any attr_* query parameter is supported.",
    ),
]


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")
    model = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    color = django_filters.CharFilter(
        field_name="variants__color",
        lookup_expr="iexact",
        distinct=True,
    )
    storage = django_filters.CharFilter(
        field_name="variants__storage",
        lookup_expr="iexact",
        distinct=True,
    )
    ram = django_filters.CharFilter(method="filter_attribute")
    sim = django_filters.CharFilter(method="filter_attribute")
    min_price = django_filters.NumberFilter(
        field_name="variants__price",
        lookup_expr="gte",
        distinct=True,
    )
    max_price = django_filters.NumberFilter(
        field_name="variants__price",
        lookup_expr="lte",
        distinct=True,
    )
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        fields = [
            "category",
            "model",
            "color",
            "storage",
            "ram",
            "sim",
            "min_price",
            "max_price",
            "in_stock",
        ]

    @staticmethod
    def filter_in_stock(queryset, name, value):
        if value:
            return queryset.filter(variants__stock__gt=0).distinct()
        return queryset

    @staticmethod
    def filter_attribute(queryset, name, value):
        if value:
            lookup = "icontains" if name == "sim" else "iexact"
            return queryset.filter(
                variants__attributes__name=name,
                **{f"variants__attributes__value__{lookup}": value},
            ).distinct()
        return queryset


class ProductVariantFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="product__category",
        lookup_expr="iexact",
    )
    model = django_filters.CharFilter(
        field_name="product__name",
        lookup_expr="icontains",
    )
    color = django_filters.CharFilter(field_name="color", lookup_expr="iexact")
    storage = django_filters.CharFilter(field_name="storage", lookup_expr="iexact")
    ram = django_filters.CharFilter(method="filter_attribute")
    sim = django_filters.CharFilter(method="filter_attribute")
    is_new = django_filters.BooleanFilter(method="filter_is_new")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = ProductVariant
        fields = [
            "category",
            "model",
            "color",
            "storage",
            "ram",
            "sim",
            "is_new",
            "min_price",
            "max_price",
            "in_stock",
        ]

    @staticmethod
    def filter_in_stock(queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    @staticmethod
    def filter_is_new(queryset, name, value):
        if value:
            now = timezone.now()
            return queryset.filter(is_new=True).filter(
                Q(new_until__isnull=True) |
                Q(new_until__gte=now)
            )
        return queryset

    @staticmethod
    def filter_attribute(queryset, name, value):
        if value:
            lookup = "icontains" if name == "sim" else "iexact"
            return queryset.filter(
                attributes__name=name,
                **{f"attributes__value__{lookup}": value},
            ).distinct()
        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="List products",
        description=(
            "Returns active products with nested variants, images, and attributes. "
            "Supports category, model, color, storage, RAM, SIM, price range, stock, "
            "search, ordering, and dynamic attr_* filters."
        ),
        parameters=ATTRIBUTE_FILTER_PARAMETERS,
        tags=["products"],
    ),
    retrieve=extend_schema(
        summary="Retrieve product by slug",
        description="Returns one product with all variants, prices, stock, images, and attributes.",
        tags=["products"],
    ),
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = [
        "name",
        "description",
        "variants__color",
        "variants__storage",
        "variants__attributes__value",
    ]
    ordering_fields = ["name", "created_at", "price", "stock"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Product.objects
            .filter(is_active=True)
            .prefetch_related(
                "variants__attributes",
                "variants__images",
            )
            .annotate(
                price=Min("variants__price"),
                stock=Sum("variants__stock"),
            )
        )

        for key, value in self.request.query_params.items():
            if key.startswith("attr_") and value:
                queryset = queryset.filter(
                    variants__attributes__name=key.removeprefix("attr_"),
                    variants__attributes__value__iexact=value,
                )

        return queryset.distinct()

    serializer_class = ProductSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List product variants as catalog cards",
        description=(
            "Returns every product variant as a separate catalog item. "
            "Use this endpoint for storefront grids where color and storage combinations "
            "should appear as separate cards."
        ),
        parameters=ATTRIBUTE_FILTER_PARAMETERS,
        tags=["variants"],
    ),
    retrieve=extend_schema(
        summary="Retrieve product variant by slug",
        description=(
            "Returns one variant card plus available variants of the same parent product "
            "for color and storage switching."
        ),
        tags=["variants"],
    ),
)
class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductVariantFilter
    search_fields = [
        "product__name",
        "product__description",
        "color",
        "storage",
        "attributes__value",
    ]
    ordering_fields = ["product__name", "price", "stock", "storage", "color"]
    ordering = ["product__name", "storage", "color"]

    def get_queryset(self):
        queryset = (
            ProductVariant.objects
            .filter(product__is_active=True)
            .select_related("product")
            .prefetch_related("attributes", "images")
        )

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "product__variants__images",
            )

        for key, value in self.request.query_params.items():
            if key.startswith("attr_") and value:
                queryset = queryset.filter(
                    attributes__name=key.removeprefix("attr_"),
                    attributes__value__iexact=value,
                )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductVariantDetailSerializer
        return ProductVariantCardSerializer
