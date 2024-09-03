from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Category, Image


class AuthIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        url = reverse('signup')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "terms": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login(self):
        User.objects.create_user(username="testuser", password="12345")
        url = reverse('login')  # URL name for login view
        data = {
            "username": "testuser",
            "password": "12345"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username="testuser").pk)


class ImageIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Nature")
        self.client.login(username="testuser", password="12345")

    def test_create_image(self):
        url = reverse('image-list')
        data = {
            "description": "A beautiful sunset",
            "file": "images/sunset.jpg",
            "category": self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Image.objects.filter(description="A beautiful sunset").exists())

    def test_get_image_list(self):
        Image.objects.create(user=self.user, category=self.category, description="A sunset", file="images/sunset.jpg")
        url = reverse('image-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A sunset")
