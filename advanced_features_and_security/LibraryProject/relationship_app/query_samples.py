from .models import Author, Book, Librarian, Library


library_name = 'NITT Lybrary'
librari = Library.objects.get(name=library_name)
books =librari.books.all()

author_name = "John Doe"
author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)

Librarian.objects.get(library=librari)