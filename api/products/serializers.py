
from rest_framework import serializers
from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter
from django_filters import CharFilter
from django_filters import rest_framework as filters
from items.models import Item


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price',
                  'currency', 'category', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price',
                  'currency', 'category', 'created_at', 'updated_at')
 

class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price',
                  'currency', 'category')