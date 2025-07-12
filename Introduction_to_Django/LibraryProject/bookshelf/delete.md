### Delete the book we have create with the command

book_delete = Book.objects.filter(title= "1984")
book_delete.delete()

### Succesfully delete the book from the DB return (0, {})