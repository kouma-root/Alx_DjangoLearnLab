### Delete the book we have create with the command
from bookshelf.models import Book
book = Book.objects.filter(title= "1984")
book.delete()

### Succesfully delete the book from the DB return (0, {})