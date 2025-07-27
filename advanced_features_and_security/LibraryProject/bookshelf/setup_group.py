from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

def setup_group_and_permissions():
    
    # Define permissions to be added to the group
    group_permissions = { 
        'Viewers': ['can_view'],
        'Editors': ['can_view','can_create', 'can_edit'],
        'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete']
    }
    
    content_type = ContentType.objects.get_for_model(Book)
    
    for group_name, permissions in group_permissions.items():
        
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Group '{group_name}' created.")
        else:
            print(f"Group '{group_name}' already exists.")
        
        group_permissions.clear()
        
        for codename in permission_codenames:
            try:
                permission = Permission.objects.get(codename=codename, content_type=content_type)
                group.permissions.add(permission)
                print(f"Permission '{codename}' added to group '{group_name}'.")
            except Permission.DoesNotExist:
                print(f"Permission '{codename}' does not exist for group '{group_name}'.")
                
        group.save()