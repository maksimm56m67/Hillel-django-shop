import decimal

from django.db import models

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency


class CurrencyHistory(PKMixin):
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sale = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    
    def __str__(self):
        return f"{self.currency} | {self.buy}| {self.sale}"
    
    @classmethod
    def last_curs(cls, currency_code, attr='sale') -> decimal.Decimal:
        return getattr(cls.objects.filter(
            currency=currency_code
        ).order_by(
            '-created_at'
        ).first(), attr, decimal.Decimal('1.00'))
        
        
class SingletonModel(models.Model):
    class Meta:
        abstract = True
 
    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)
 
    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Config(SingletonModel):
    contact_form_email = models.EmailField()
    
    def __str__(self):
        return 'Configuration'