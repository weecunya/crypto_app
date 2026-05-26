from .permissions import has_permission
from django.http import JsonResponse
from functools import wraps

def permission_required(resource_name:str,operation:str):
    def decorator(f):
        @wraps(f)
        def wrapper(request,*args,**kwargs):
            if not request.user:
                return JsonResponse({'error':'user not logged in'}, status=401)
            if not has_permission(request.user,resource_name,operation):
                return JsonResponse({'error':'user does not have permission'}, status=403)
            return f(request,*args,**kwargs)
        return wrapper
    return decorator
