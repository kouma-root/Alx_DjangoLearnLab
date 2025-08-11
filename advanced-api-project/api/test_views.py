from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITests(APITestCase):
    """Test suite for the Book API endpoints."""

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create an author
        self.author = Author.objects.create(name="Jane Austen")

        # Create some books
        self.book1 = Book.objects.create(title="Pride and Prejudice", publication_year=1813, author=self.author)
        self.book2 = Book.objects.create(title="Sense and Sensibility", publication_year=1811, author=self.author)

        # Endpoints
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book1.id])
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', args=[self.book1.id])
        self.delete_url = reverse('book-delete', args=[self.book1.id])

    # ---------- LIST & DETAIL ----------
    def test_list_books(self):
        """Test retrieving all books (public access)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """Test retrieving one book by ID (public access)"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Pride and Prejudice")

    # ---------- CREATE ----------
    def test_create_book_requires_authentication(self):
        """Test that creating a book requires login"""
        payload = {
            "title": "Emma",
            "publication_year": 1815,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Test that authenticated user can create a book"""
        self.client.login(username='testuser', password='testpass')
        payload = {
            "title": "Emma",
            "publication_year": 1815,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ---------- UPDATE ----------
    def test_update_book_authenticated(self):
        """Test updating a book requires authentication"""
        self.client.login(username='testuser', password='testpass')
        payload = {
            "title": "Pride and Prejudice (Updated)",
            "publication_year": 1813,
            "author": self.author.id
        }
        response = self.client.put(self.update_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Pride and Prejudice (Updated)")

    # ---------- DELETE ----------
    def test_delete_book_authenticated(self):
        """Test deleting a book requires authentication"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # ---------- FILTERING ----------
    def test_filter_books_by_year(self):
        """Test filtering books by publication_year"""
        url = f"{self.list_url}?publication_year=1811"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Sense and Sensibility")

    # ---------- SEARCH ----------
    def test_search_books_by_title(self):
        """Test searching for books by title"""
        url = f"{self.list_url}?search=Sense"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Sense and Sensibility")

    # ---------- ORDERING ----------
    def test_order_books_by_year_desc(self):
        """Test ordering books by publication_year descending"""
        url = f"{self.list_url}?ordering=-publication_year"
        response = self.client.get(url)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))