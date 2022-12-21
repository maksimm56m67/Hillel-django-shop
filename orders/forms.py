from django import forms
from django.core.exceptions import ValidationError

from items.models import Item
from orders.models import Discount

class UpdateCartOrderForm(forms.Form):
    product = forms.UUIDField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']

    def clean(self):
        # todo divide logic
        product_id = self.cleaned_data.get('product')
        if product_id:
            try:
                Item.objects.get(id=product_id)
            except Item.DoesNotExist:
                raise ValidationError('Wrong product id.')
        return self.cleaned_data

    def save(self, action):
        if action == 'clear':
            self.instance.items.clear()
            return
        elif action == 'pay':
            self.instance.pay()
            return
        getattr(self.instance.items, action)(self.cleaned_data['product'])


class RecalculateCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']
        self.fields = {k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                       k.startswith(('quantity', 'item'))}

    def save(self):
        """
        {'quantity_0': 2,
        'item_0': UUID('e04bc1aa-dc11-4791-a187-5118ea5ce01a'),
        'item_1': 2,
        'item_2': UUID('4e26895f-2056-4c57-ad53-3a09c9861b56'),
        'item_3': 3,
        'item_4': UUID('f6177123-adb7-4237-bc3e-8a5d2aabae6e')}
        :return: instance
        """
        for k in self.cleaned_data.keys():
            if k.startswith('item_'):
                index = k.split('_')[-1]
                self.instance.items.through.objects \
                    .filter(order=self.instance,
                            item_id=self.cleaned_data[f'item_{index}']) \
                    .update(quantity=self.cleaned_data[f'quantity_{index}'])
        return self.instance


class ApplyDiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('code',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.order = kwargs['order']

    def clean_code(self):
        try:
            self.instance = Discount.objects.get(
                code=self.cleaned_data['code'],
                is_active=True
            )
        except Discount.DoesNotExist:
            raise ValidationError('Wrong discount code.')
        return self.cleaned_data['code']

    def apply(self):
        self.order.discount = self.instance
        self.order.save(update_fields=('discount',))
