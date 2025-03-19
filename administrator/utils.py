from functools import wraps

# Check if uer is authenticated  decorator
# redirect unauthenticated to sign in page
def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('signin')  # Redirect to login page if not authenticated
    return _wrapped_view


# RBAC Role Based Access Control

def is_admin(user):
	return user.is_authenticated and user.groups.filter(name="admin").exists()

def is_business(user):
	return user.is_authenticated and user.groups.filter(name="business").exist()

def is_customer(user):
	return user.is_authenticated and user.groups.filter(name="customer").exist()

def is_moderator(user):
	return user.is_authenticated and user.groups.filter(name="moderator").exist()

def is_courier(user):
	return user.is_authenticated and user.groups.filter(name="courier").exist()

