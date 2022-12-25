import csv
import decimal

from io import StringIO

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from items.models import Item, Category
from shop.model_choices import Currency

class ContactForm(forms.Form):
    email = forms.EmailField(label='Email')
    text = forms.CharField(label='Text',widget=forms.Textarea)


class ImportCSVForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )

    def clean_file(self):
        csv_file = self.cleaned_data['file']
        reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))
        products_list = []
        for product in reader:
            try:
                products_list.append(
                    Item(
                        name=product['name'],
                        description=product['description'],
                        price=decimal.Decimal(product['price']),
                        category=Category.objects.get_or_create(
                            name=product['category']
                        )[0]
                    )
                )
            except (KeyError, decimal.InvalidOperation) as err:
                raise ValidationError(err)
        if not products_list:
            raise ValidationError('Wrong file format.')
        return products_list

    def save(self):
        products_list = self.cleaned_data['file']
        Item.objects.bulk_create(products_list)
        
class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label="Select"
    )
    currency = forms.ChoiceField(
        required=False,
        choices=[('', 'Select')] + Currency.choices,
    )
    name = forms.CharField(max_length=255, required=False)
    
    