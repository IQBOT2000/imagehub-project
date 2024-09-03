from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Category, Image


class UserIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_registration_and_login(self):
        registration_url = reverse('signup')
        registration_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
            "terms": "on"
        }
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username="newuser")
        self.assertIsNotNone(user)

        login_url = reverse('login')
        login_data = {
            "username": "newuser",
            "password": "testpassword"
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, "Welcome")

        self.client.login(username="newuser", password="testpassword")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome newuser")


class ImageIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Nature")
        self.client.login(username="testuser", password="12345")

    def test_upload_image(self):
        upload_url = reverse('image-list')
        image_data = {
            "description": "A beautiful sunset",
            "file": "images/sunset.jpg",
            "category": self.category.id
        }

        response = self.client.post(upload_url, image_data, format='multipart')
        self.assertEqual(response.status_code, 201)

        image = Image.objects.get(description="A beautiful sunset")
        self.assertIsNotNone(image)

    def test_view_images(self):
        Image.objects.create(user=self.user, category=self.category, description="A sunset", file="images/sunset.jpg")

        view_url = reverse('image-list')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A sunset")
