from django.core.exceptions import PermissionDenied
from functools import wraps

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        
        is_teacher = request.user.groups.filter(name = 'Учителя').exists()
        if request.user.is_superuser or is_teacher:
            return view_func(request, *args, **kwargs)

        raise PermissionDenied
    
    return _wrapped_view