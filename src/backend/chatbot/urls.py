from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'chatbot', views.ChatbotViewSet, basename='chatbot')

urlpatterns = router.urls
