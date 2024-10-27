from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path


router = DefaultRouter()
router.register(r'chatbot', views.ChatbotViewSet, basename='chatbot')

urlpatterns = router.urls


urlpatterns = [
    path('upload/pdf/', views.upload_file, name='upload_pdf'),  
    path('upload/file/', views.upload_admindata, name='upload_admin'),  
] + router.urls