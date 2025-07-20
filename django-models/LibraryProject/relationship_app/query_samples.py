from .models import Author, Book, Librarian, Library


library_name = 'NITT Lybrary'
library = Library.objects.get(name=library_name)
books =library.books.all()

author_name = "John Doe"
author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)


library = Library.objects.get(name=library_name)
Librarian.objects.get(library = library)