from django.test import TestCase, Client
from django.contrib.auth.models import User
from youtube.accounts.forms import CustomUserCreationForm


class CustomUserFormTest(TestCase):
    """Simple tests for CustomUserCreationForm"""

    def test_valid_form(self):
        """Test form with valid data"""
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertTrue(form.is_valid())

    def test_form_saves_email(self):
        """Test that email is saved"""
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.email, 'test@example.com')


class UserRegisterViewTest(TestCase):
    """Simple tests for user registration"""

    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        """Test register page loads"""
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        """Test registration creates user"""
        response = self.client.post('/accounts/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())


class UserProfileViewTest(TestCase):
    """Simple tests for user profile"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_profile_requires_login(self):
        """Test profile requires authentication"""
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)

    def test_profile_loads_authenticated(self):
        """Test profile loads when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

