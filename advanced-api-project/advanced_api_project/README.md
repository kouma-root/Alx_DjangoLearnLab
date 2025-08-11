# Advanced API Project — Book Views

This API provides CRUD functionality for books using Django REST Framework's generic views.

Endpoints:
- GET /api/books/ — List all books (public)
- GET /api/books/<id>/ — Retrieve one book (public)
- POST /api/books/create/ — Create a new book (auth only)
- PUT /api/books/<id>/update/ — Update a book (auth only)
- DELETE /api/books/<id>/delete/ — Delete a book (auth only)

Permissions:
- Read operations are open to everyone.
- Create, update, delete operations require authentication.


## Filtering, Searching, and Ordering

You can filter, search, and order books using query parameters:

### Filtering:
- /api/books/?title=BookTitle
- /api/books/?publication_year=2020
- /api/books/?author=1

### Searching:
- /api/books/?search=Python
- /api/books/?search=Austen

### Ordering:
- /api/books/?ordering=title
- /api/books/?ordering=-publication_year