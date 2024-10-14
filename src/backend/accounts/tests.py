from django.test import TestCase
from .models import User, Profile

class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='password123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser3')
        self.assertEqual(self.user.email, 'testuser3@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_auto_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.full_name, self.user.username)
        self.assertEqual(self.user.profile.user, self.user)

    def tearDown(self):
        self.user.delete()

class ProfileUpdateTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
            password='password123'
        )
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_update(self):
        self.profile.full_name = "Updated User"
        self.profile.phone = "0987654321"
        self.profile.address = "456 Updated Street"
        self.profile.save()

        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.full_name, "Updated User")
        self.assertEqual(updated_profile.phone, "0987654321")
        self.assertEqual(updated_profile.address, "456 Updated Street")

    def tearDown(self):
        self.profile.delete()
        self.user.delete()

class RegistrationTests(TestCase):

    def test_user_registration(self):
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpassword123'
        )
        self.assertEqual(User.objects.last().username, 'newuser')
        self.assertTrue(hasattr(user, 'profile'))  
        self.assertEqual(user.profile.full_name, 'newuser')  
        user.delete()

class PasswordChangeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='password1234'
        )

    def test_change_password(self):
        self.user.set_password('newpassword123')
        self.user.save()

        self.assertTrue(self.user.check_password('newpassword123'))

    def tearDown(self):
        self.user.delete()
