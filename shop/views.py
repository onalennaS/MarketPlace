from django.shortcuts import render, redirect
from functools import wraps
from seller.wrap_models.product_model import Product, Extras
from user.wrap_models.cart_models import Cart, Wishlist

def get_cart_items(user):
    return Cart.objects.filter(user=user).all().count()
def get_wishlist_items(user):
    return Wishlist.objects.filter(user=user).all().count()

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


def shop_base(request):
    products = Product.objects.filter(status="active").all()
    items = get_cart_items(request.user)
    return render(request,'products/shop.html',{'products':products,'cart_items_count':items})


def view_product(request, product_id):
    product = Product.objects.filter(id=int(product_id)).first()
    items = get_cart_items(request.user)

    if product:
        return render(request,'products/view_product.html',{'product':product,'cart_items_count':items,"wishlist_items_count":get_wishlist_items(request.user)})
    return render(request,'products/view_product.html')