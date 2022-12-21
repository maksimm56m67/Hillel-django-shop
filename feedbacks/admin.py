import re

from django.contrib import admin

from feedbacks.models import Feedback




@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ('text', 'user', 'rating')
