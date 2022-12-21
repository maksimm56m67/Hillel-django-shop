import re
from django import forms

from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text', 'user', 'rating')
        
    def clean_text(self):
        return re.sub(r'[^\w\s]+|[\d]+', r'', self.cleaned_data.get('text')).strip()
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
