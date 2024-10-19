from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'prediction', views.StockPredictionViewSet, basename='machine-learning')


# app_name='predictions'
urlpatterns = [
    path('', include(router.urls)),

]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.Data.as_view(),name='data')
# ]
