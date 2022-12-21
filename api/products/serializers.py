
from rest_framework import serializers
from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter
from django_filters import CharFilter

from items.models import Item


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name')
 

class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name')