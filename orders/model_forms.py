from django import forms

from orders.models import Order 
from django.forms import NumberInput

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('total_amount', 'items', 'user', 'discount')
        
	

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
        
