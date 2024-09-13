from django.urls import path
from . import views

urlpatterns = [
    path('', views.Data.as_view(),name='data')
]