from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'machine-learning', views.PredictionViewSets, basename='ml')


app_name='predictions'
urlpatterns = [
    path('', include(router.urls)),

]
