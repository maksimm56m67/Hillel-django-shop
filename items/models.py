from django.db import models

import decimal
import io

from django.core.cache import cache
from shop.model_choices import Currency
from shop.mixins.models_mixins import PKMixin
from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from currencies.models import CurrencyHistory
from django.db.models import Case, When, Sum, F
from django.contrib.auth import get_user_model

from datetime import timedelta
from django.utils import timezone
from shop.celery import app

from os import path
from shop.api_clients import BaseClient
from django.core.files.images import ImageFile

from items.client.client import products_parser

from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, \
    BEFORE_UPDATE, AFTER_CREATE, BEFORE_CREATE, BEFORE_SAVE

def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/' \
           f'{instance.pk}/image{extension}'

class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.name

class Item(LifecycleModelMixin, PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_image, blank=True)
    price = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UAH)
    total_price = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    items = models.ManyToManyField('items.Item', blank=True)

    def __str__(self):
        return f"{self.name} | {self.category}| {self.price}"

    @classmethod
    def _cache_key(cls):
        return 'products'

    @classmethod
    def get_products(cls):
        products = cache.get(cls._cache_key())
        if not products:
            products = Item.objects.all()
            cache.set(cls._cache_key(), products)
        return products

    @property
    def exchange_price(self):
        key = f'exchange_price_{self.id}'
        exchange_price = cache.get(key)
        if not exchange_price:
            exchange_price = round(self.price * self.curs, 2)
            cache.set(key, exchange_price)
        return exchange_price

    @property
    def curs(self) -> decimal.Decimal:
        return CurrencyHistory.last_curs(self.currency)
    
    @app.task
    def clear_old_currencies(self):             
        Item.objects.filter(
            created_at__lt=timezone.now() - timedelta(days=1),        
            total_price=self.price * self.curs
        ).save()
   
      
    @hook(AFTER_UPDATE)
    def order_is_paid(self): 
        self.total_price = self.price * self.curs
        self.save(update_fields=('total_price',), skip_hooks=True)  
                  
    @hook(AFTER_CREATE)
    def order_is_paid(self): 
        self.total_price = self.price * self.curs
        self.save(update_fields=('total_price',), skip_hooks=True)   
          




class FavoriteProduct(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='favorite_products'
    )
    items = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='in_favorites'
    )

    class Meta:
        unique_together = ('user', 'items')
    
    




