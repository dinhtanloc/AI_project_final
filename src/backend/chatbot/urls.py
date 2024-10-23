from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path


router = DefaultRouter()
router.register(r'chatbot', views.ChatbotViewSet, basename='chatbot')

urlpatterns = router.urls


urlpatterns = [
    path('upload/pdf/', views.upload_pdf, name='upload_pdf'),  # Thêm URL cho hàm upload_pdf
] + router.urls