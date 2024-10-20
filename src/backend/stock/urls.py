from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stocktracking', views.StockTracking, basename='stock')

urlpatterns = router.urls
