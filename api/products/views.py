from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.products.serializers import ProductSerializer, ProductRetrieveSerializer, ProductFilter

from items.models import Item

from django_filters import rest_framework as filters


class ProductsViewList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProductsViewRetrieve(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    
class ProductList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    



