from django.urls import path
from rest_framework import views
from .views import test
urlpatterns = [
   path('test',test,name='register'),
]