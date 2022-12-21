from django.urls import path

from feedbacks import views

urlpatterns = [
    path('', views.feedbacks, name='feedbacks'), 
    #http://127.0.0.1:8000/feedbacks/
]