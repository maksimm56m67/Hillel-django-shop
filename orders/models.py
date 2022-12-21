import decimal

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from datetime import timedelta
from django.utils import timezone

from shop.celery import app

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.model_choices import DiscountTypes
from items.models import Item

from shop.mixins.models_mixins import PKMixin
from django.db.models import Case, When, Sum, F
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, \
    BEFORE_UPDATE, AFTER_CREATE, BEFORE_CREATE
# Create your models here.


class Discount(PKMixin):
    amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0)
    code = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    discount_type = models.PositiveSmallIntegerField(choices=DiscountTypes.choices, default=DiscountTypes.VALUE)

    def __str__(self):
        return f"{self.amount} | {self.code} | " \
               f"{DiscountTypes(self.discount_type).label}"
               

class Order(LifecycleModelMixin, models.Model):
    total_amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0)
    items = models.ManyToManyField("items.Item", through='orders.OrderItemRelation') # а в through ты как и говорим чтоб место класической джаговской, использовать науш модель OrderItemRelation 
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.ForeignKey( Discount, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        # Делает так чтоб в один момент времени какой то юзер с полем is_active существовал только один раз. 
        constraints = [
            models.UniqueConstraint(fields=['user'], condition=models.Q(is_active=True), name='unique_is_active')
        ]
        
    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid
    

    @app.task
    def clear_old_currencies():
        Order.objects.filter(
            created_at__lt=timezone.now() - timedelta(days=3),
            is_active = True
        ).delete()

    def get_products_through(self):
        return self.items.through.objects \
            .filter(order=self) \
            .select_related('item') \
            .annotate(full_price=F('item__price') * F('quantity'))


    def get_total_amount(self):
        total_amount = 0
        for product_relation in self.get_products_through().iterator():
            total_amount += product_relation.full_price * product_relation.item.curs  # noqa

        if self.discount:
            total_amount = (
                total_amount - self.discount.amount
                if self.discount.discount_type == DiscountTypes.VALUE else
                total_amount - (
                        self.total_amount / 100 * self.discount.amount
                )
            ).quantize(decimal.Decimal('.01'))
        return total_amount
  

        
    @hook(AFTER_UPDATE)
    def order_after_update(self):
        if self.items.exists():
            self.total_amount = self.get_total_amount()
            self.save(update_fields=('total_amount',), skip_hooks=True)

   
    
    @hook(BEFORE_UPDATE, when='is_paid', has_changed=True, was=False)
    def order_is_paid(self):
        self.is_active = False  	
        # Order.objects.filter(is_active = False).delete() 

    def pay(self):
        self.is_paid = True
        self.save()        
            
# Это таже самая модель которая создаеться при отоншении один ко многим. Но мы написали своб чтоб мы могли добавить поле quantity.
class OrderItemRelation(PKMixin):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        'items.Item',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'item')