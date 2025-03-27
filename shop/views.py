from django.shortcuts import render, redirect
from functools import wraps
from seller.wrap_models.product_model import Product, Extras
from seller.wrap_models.business_model import BusinessInformation, Address
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
    businesses = list(BusinessInformation.objects.all())  # Convert QuerySet to a list for efficient slicing
    businesse_list = [businesses[i:i+2] for i in range(0, len(businesses), 2)]

    items= 0
    if request.user.is_authenticated:
        items = get_cart_items(request.user)
    return render(request,'products/shop1.html',{'products':products,'cart_items_count':items,'business_list':businesse_list}) 


def view_business_products(request,business_id):
    products = Product.objects.filter(status="active").all()
    business = BusinessInformation.objects.filter(id=int(business_id)).first()  # Get the first business object
    products = Product.objects.filter(business=business).all()  # Get all products for the business
    address = Address.objects.filter(business=business).first()  # Get the first address for the business

    # Initialize an empty dictionary to hold categories and their corresponding products
    categories = {}

    # Loop through the products and group them by category
    for product in products:
        category = product.category
        # Initialize the category list if it doesn't exist in the dictionary
        if category not in categories:
            categories[category] = []
        categories[category].append(product)

    return render(request,'products/business_products.html',{'business':business,'categories':categories, 'address':address}) 


@login_required_custom
def view_product(request, product_id):
    product = Product.objects.filter(id=int(product_id)).first()
    items= 0
    if request.user.is_authenticated:
        items = get_cart_items(request.user)
    if product:
        return render(request,'products/view_product.html',{'product':product,'cart_items_count':items,"wishlist_items_count":get_wishlist_items(request.user)})
    return render(request,'products/view_product.html')


def home(request):
    return render(request,'products/landing_page.html')