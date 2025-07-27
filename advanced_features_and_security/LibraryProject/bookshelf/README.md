## 🔐 Permissions and Groups Setup Guide

This application uses Django's built-in permission system to manage user access for the `Article` model.

### ✅ Model-Level Permissions
The following custom permissions are defined in `Article`:

| Permission Codename | Description              |
|---------------------|--------------------------|
| can_create          | Can create an article    |
| can_edit            | Can edit an article      |
| can_delete          | Can delete an article    |

These are defined inside the `Meta` class of the `Article` model.

---

### 👥 User Groups

We use Django `Group` objects to bundle and assign permissions:

| Group Name | Assigned Permissions                   |
|------------|-----------------------------------------|
| Admins     | can_create, can_edit, can_delete        |
| Editors    | can_create, can_edit                    |
| Viewers    | No permissions (can only read articles) |

You can manage these groups using the Django Admin interface or by running a setup script (see `create_groups.py`).

---

### 🛡️ Permission Enforcement

We use `@permission_required()` in views to restrict access:

```python
@permission_required('yourapp.can_edit', raise_exception=True)
def edit_article(request, pk):
    ...


# Security Overview

## 1. Permissions and Groups
- Custom permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
- Groups: `Viewers`, `Editors`, `Admins`
- Each view checks required permissions using `@permission_required`.

## 2. Middleware & CSP
- Custom middleware sets the `Content-Security-Policy` header to restrict content to trusted sources.

## 3. Settings
- `DEBUG = False` for production
- Enabled XSS filter, content type nosniff, and secure cookies
- Cookies (`CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE`) are only sent over HTTPS

## 4. CSRF
- All forms use `{% csrf_token %}` in templates

## 5. ORM Safety
- All user input is processed through Django's ORM or forms
- No raw SQL queries are used

## 6. Testing
- Manual testing for:
  - CSRF tokens present in forms
  - Safe query handling
  - Permission enforcement
  - CSP header presence


  ## 🔐 1. Manual Django Security Settings (`settings.py`)

The following changes were **manually applied** in `settings.py` to secure the application:

### ✅ Basic Security

```python
# Never run with DEBUG = True in production
DEBUG = False

# Only allow known domains
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']