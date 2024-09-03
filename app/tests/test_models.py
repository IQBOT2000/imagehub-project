from django.contrib.auth.models import User
from django.test import TestCase

from .models import Category, Image


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Nature")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Nature")

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), "Nature")

    def test_category_update(self):
        self.category.name = "Wildlife"
        self.category.save()
        self.assertEqual(self.category.name, "Wildlife")

    def test_category_delete(self):
        category_id = self.category.id
        self.category.delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)


class ImageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Nature")
        self.image = Image.objects.create(
            user=self.user,
            category=self.category,
            description="A beautiful sunset",
            file="images/sunset.jpg"
        )

    def test_image_creation(self):
        self.assertEqual(self.image.description, "A beautiful sunset")
        self.assertEqual(self.image.file, "images/sunset.jpg")

    def test_image_update(self):
        self.image.description = "An updated description"
        self.image.save()
        self.assertEqual(self.image.description, "An updated description")

    def test_image_delete(self):
        image_id = self.image.id
        self.image.delete()
        with self.assertRaises(Image.DoesNotExist):
            Image.objects.get(id=image_id)
