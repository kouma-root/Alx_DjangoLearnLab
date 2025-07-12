### Update the title of book 1984 with the command

book_update = Book.objects.filter(title= "1984")
book_update.title= "Nineteen Eighty-Four"

### The title of the book is succesfully updated return 1
