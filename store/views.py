from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Product.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer
        return ProductSerializer
