"""
Unit Testing Strategy for DRF APIs

This test suite covers:
- CRUD operations for Book model
- Filtering by publication_year
- Searching by title
- Ordering by title
- Permission enforcement for authenticated access

How to run:
$ python manage.py test api

Expected:
- All tests pass with correct status codes and data integrity
- Failures indicate issues in views, serializers, or permissions
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.author = Author.objects.create(name="Tsitsi Dangarembga")
        self.book = Book.objects.create(
            title="Nervous Conditions",
            publication_year=1988,
            author=self.author
        )

    def test_create_book(self):
        data = {
            "title": "The Book of Not",
            "publication_year": 2006,
            "author": self.author.id
        }
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "The Book of Not")

    def test_update_book(self):
        response = self.client.patch(f"/api/books/{self.book.id}/", {"title": "Nervous Conditions - Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nervous Conditions - Updated")

    def test_delete_book(self):
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filter_books_by_year(self):
        response = self.client.get("/api/books/?publication_year=1988")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        response = self.client.get("/api/books/?search=Nervous")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Nervous Conditions", response.data[0]["title"])

    def test_order_books_by_title(self):
        Book.objects.create(title="This Mournable Body", publication_year=2018, author=self.author)
        response = self.client.get("/api/books/?ordering=title")
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/books/", {
            "title": "Unseen Book",
            "publication_year": 2025,
            "author": self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

