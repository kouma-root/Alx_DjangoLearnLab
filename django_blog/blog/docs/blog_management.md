# Blog Post Management (django_blog)

## Features
- List all posts (`/posts/`)
- View post detail (`/posts/<id>/`)
- Create new post (`/posts/new/`) — login required
- Edit post (`/posts/<id>/edit/`) — only author
- Delete post (`/posts/<id>/delete/`) — only author

## Permissions
- Public: list + detail
- Authenticated: create
- Author-only: update & delete

## Notes
- Post author auto-set as logged-in user
- Uses Django class-based views with LoginRequiredMixin & UserPassesTestMixin