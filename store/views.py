from django.db.models import Min, Sum
from django_filters import rest_framework as django_filters
from rest_framework import filters
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")
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
        fields = ["category", "color", "storage", "min_price", "max_price", "in_stock"]

    @staticmethod
    def filter_in_stock(queryset, name, value):
        if value:
            return queryset.filter(variants__stock__gt=0).distinct()
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
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

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer
        return ProductSerializer
