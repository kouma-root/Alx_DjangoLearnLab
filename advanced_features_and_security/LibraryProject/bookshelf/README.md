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