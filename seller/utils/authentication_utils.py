from django.shortcuts import  redirect
from functools import wraps

def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('signin')  # Redirect to login page if not authenticated
    return _wrapped_view

def has_password(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.password.startswith("pbkdf2"):
                return view_func(request, *args, **kwargs)
            return redirect('create_password')
    return _wrapped_view

def verify_role(roles, redirect_url='not_allowed'):
    if isinstance(roles, str):
        roles = [roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name__in=roles).exists():
                return view_func(request, *args, **kwargs)
            return redirect(redirect_url)
        return _wrapped_view
    return decorator


    

   