from django.shortcuts import render
from django.http import JsonResponse
from .models import User,Profile
from rest_framework.views import APIView
from rest_framework import status,viewsets

from .serializers import MyTokenObtainPairSerializer , RegisterSerializer,ProfileSerializer,ChangePasswordSerializer, StaffTokenObtainPairSerializer,UserSerializer
from django.http import JsonResponse

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsStaffUser


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='')
    def get_routes(self, request):
        routes = [
            '/api/token/',
            '/api/register/',
            '/api/token/refresh/'
        ]
        return Response(routes)

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated], url_path='current-user')
    def test_endpoint(self, request):
        if request.method == 'GET':
            user_info = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            }
            return Response({'response': user_info}, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            text = "Hello buddy"
            data = f'Congratulations, your API just responded to POST request with text: {text}'
            return Response({'response': data}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='staff')
    def is_staff_endpoint(self, request):
        is_staff = request.user.is_staff
        serializer = UserSerializer(request.user)
        return Response({"is_staff": is_staff, "staff": serializer.data})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsStaffUser], url_path='staff-list')
    def staff_list_view(self, request):
        staff_users = User.objects.filter(is_staff=True)
        serializer = UserSerializer(staff_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated], url_path='profile')
    def profile_view(self, request):
        user_profile = Profile.objects.get(user=request.user)
        if request.method == 'GET':
            serializer = ProfileSerializer(user_profile)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = ProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if 'image' in request.FILES:
                    image_file = request.FILES.get('image')
                    user_profile.image = image_file
                    user_profile.save()
                if 'current_password' in request.data and 'new_password' in request.data and 'confirm_password' in request.data:
                    current_password = request.data['current_password']
                    new_password = request.data['new_password']
                    confirm_password = request.data['confirm_password']
                    if not request.user.check_password(current_password):
                        return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
                    if new_password != confirm_password:
                        return Response({'error': 'New password and confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)
                    request.user.set_password(new_password)
                    request.user.save()
                    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


