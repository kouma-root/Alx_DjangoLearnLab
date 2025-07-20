from .models import Author, Book, Librarian, Library


library_name = 'NITT Lybrary'
books = Library.objects.get(name=library_name)
books.objects.all()
library_book = Book.objects.get(library='Kouma')

librarian = Librarian.objects.get(library='kouma')