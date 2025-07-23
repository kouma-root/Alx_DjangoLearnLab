from django.http import HttpResponseForbidden
from functools import wraps

##def role_required(*roles):
    
  ##  def decorator(view_func):
    #    @wraps(view_func)
     #   def _wrapped_view(request, *args, **kwargs):
      #      profile = getattr(request.user, 'userprofile', None)
       #     if profile and profile.role in roles :
        #        return view_func(request, *args, **kwargs)
         #   return HttpResponseForbidden("You do not have permission to access this page")
     #   return _wrapped_view
   # return decorator
##

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'member'


