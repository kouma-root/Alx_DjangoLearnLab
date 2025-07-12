### import the model in the shel with the following command

# from bookshelf.models import Book

### create a  new_book  with the following command

Book.objects.create(title="1984", author= "George Orwell", publication_year=1949)

## The new object is saved in the DB succesfully