from django.urls import path
from . import views

urlpatterns = [
    path('', views.cars_view, name='cars_list')
]