from django.db import models

class Author(models.Model):
    # Author's full name
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=255)
    # Year published
    publication_year = models.IntegerField()
    # Relationship: One author can have many books
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title