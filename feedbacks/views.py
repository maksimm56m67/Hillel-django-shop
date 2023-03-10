
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback
from items.models import Item



@login_required
def feedbacks(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        form = FeedbackModelForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FeedbackModelForm(user=user)
    context = {
        'feedbacks': Feedback.objects.all(),
        'form': form
    }
    return render(request, 'feedbacks/feedbacks.html', context)




