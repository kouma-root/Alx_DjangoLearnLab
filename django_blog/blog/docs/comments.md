# Comment System

## Overview
Adds per-post comments with create, edit, delete. Only comment authors may edit or delete their comments. Anonymous users can read but must log in to post.

## Routes
- Create:  `POST /posts/<post_id>/comments/new/` (form shown on post detail)
- Update:  `GET/POST /comments/<id>/edit/` (author only)
- Delete:  `POST /comments/<id>/delete/` (author only)
- List:    `GET /posts/<post_id>/comments/` (optional standalone list)
- Post detail shows all comments and the creation form when authenticated.

## Security
- Uses `LoginRequiredMixin` for create/update/delete.
- Uses `UserPassesTestMixin` to restrict update/delete to the comment’s author.
- CSRF protection on all forms.
- Server-side validation ensures non-empty content.

## Usage
1. Open a post detail page.
2. If logged in, submit the comment form.
3. Edit/Delete links appear only on your own comments.