from django.shortcuts import render, redirect
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
        if request.user.password.startswith("pbkdf2"):
            return view_func(request, *args, **kwargs)
        return redirect('create_password')
    return _wrapped_view

# Create your views here.
# Create your views here.

@login_required_custom
def register_business(request):
    return render(request, 'seller/register_business.html')

@login_required_custom
def register_business_form(request):
    return render(request, 'seller/register_business_form.html')

@login_required_custom
def business_status(request):
    return render(request, 'seller/businness_status.html')

@has_password
def base(request):
    return render(request, 'seller/seller_profile.html')

@login_required_custom
@has_password
def user_profile(request):
    return render(request, 'seller/seller_profile.html')

@login_required_custom
def business_info(request):
    
    return render(request, 'seller/business_info.html')
@login_required_custom
def dashboard(request):
    
    return render(request, 'seller/dashboard.html')

@login_required_custom
def view_stats(request):
   
    return render(request, 'seller/view_stats.html')

@login_required_custom
def add_products(request):
   
    return render(request, 'seller/add_products.html')

@login_required_custom
def manage_product(request):
   
    return render(request, 'seller/manage_product.html')

@login_required_custom
def edit_products(request):
   
    return render(request, 'seller/edit_product.html')

@login_required_custom
def orders(request):
    
    return render(request, 'seller/orders.html')

@login_required_custom
def order_tracking(request):
    
    return render(request, 'seller/order_tracking.html')

@login_required_custom
def transaction(request):
   
    return render(request, 'seller/sales.html')

@login_required_custom
def pay_for_premium(request):
    
    return render(request, 'seller/pay_for_premium.html')

@login_required_custom
def reviews(request):
    
    return render(request, 'seller/reviews.html')
