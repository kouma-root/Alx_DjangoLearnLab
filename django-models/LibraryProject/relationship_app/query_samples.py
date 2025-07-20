from .models import Author, Book, Librarian, Library



books = Book.objects.get(author='kouma')

library_book = Book.objects.get(library='Kouma')

librarian = Librarian.objects.get(library='kouma')