from rest_framework.test import APITestCase 
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import User, Profile

class UserModelTests(APITestCase):  

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            full_name='Test User',
            phone='1234567890',
            address='123 Test Street',
            job='Tester',
            bio='Just a test user',
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_profile_creation(self):
        self.assertEqual(self.profile.full_name, 'Test User')
        self.assertEqual(self.profile.user, self.user)

class UserAPITests(APITestCase):  

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_current_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('current-user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response']['username'], 'testuser')

    def test_update_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(reverse('profile'), {
            'full_name': 'Updated User',
            'phone': '0987654321',
            'address': '456 Updated Street'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.full_name, 'Updated User')

class RegistrationAPITests(APITestCase):  

    def test_user_registration(self):
        response = self.client.post(reverse('accounts:auth_register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.last().username, 'newuser')

class PasswordChangeAPITests(APITestCase):  

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.token = Token.objects.create(user=self.user)

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(reverse('accounts:profile'), {
            'current_password': 'password123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))



# python manage.py test
# python manage.py test myapp
# python manage.py test myapp.tests.MyModelTest
