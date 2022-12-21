from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.products.serializers import ProductSerializer, ProductRetrieveSerializer

from items.models import Item


class ProductsViewList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]



class ProductsViewRetrieve(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ProductRetrieveSerializer
    #permission_classes = [IsAuthenticated, IsAdminUser]

