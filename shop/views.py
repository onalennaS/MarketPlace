from django.shortcuts import render, redirect
from functools import wraps
from seller.wrap_models.product_model import Product, Extras
from seller.wrap_models.business_model import BusinessInformation, Address, BusinessRating
from user.wrap_models.cart_models import Cart, Wishlist
from django.http import HttpResponse
import random
from seller.utils.authentication_utils import has_password


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




def shop_base(request):
    products = list(Product.objects.filter(status="active").all())
    random.shuffle(products)
    products = products[:6]
    businesses = list(BusinessInformation.objects.all())  # Convert QuerySet to a list for efficient slicing
    businesse_list = [businesses[i:i+2] for i in range(0, len(businesses), 2)]

    items= 0
    wishlist_items_count = 0
    if request.user.is_authenticated:
        items = get_cart_items(request.user)
        wishlist_items_count = get_wishlist_items(request.user)
    most_bought = Product.objects.filter(sales__gt=8).order_by('-sales')[:10]
    return render(request,'products/shop1.html',{'most_bought':most_bought,'flash_deal_products':products,'cart_items_count':items,'wishlist_items_count':wishlist_items_count,'business_list':businesse_list})


def view_business_products(request,slug):
    products = Product.objects.filter(status="active").all()
    business = BusinessInformation.objects.filter(slug=slug).first()  # Get the first business object
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
    
    all_ratings = BusinessRating.objects.filter(business=business)
    stars_list = [rating.stars for rating in all_ratings]

    if stars_list:
        average_rating = round(sum(stars_list) / len(stars_list), 1)
    else:
        average_rating = 0.0 
    total_rating = len(stars_list)

    absolute_page_url = request.build_absolute_uri()
    absolute_image_url = None
    try:
        if business.image:
            absolute_image_url = request.build_absolute_uri(business.image.url)
    except Exception as e:
        pass
    items= 0
    wishlist_items_count = 0
    if request.user.is_authenticated:
        items = get_cart_items(request.user)
        wishlist_items_count = get_wishlist_items(request.user)
    return render(request,'products/business_products.html',{'cart_items_count':items,"wishlist_items_count":wishlist_items_count,'absolute_page_url':absolute_page_url,'absolute_image_url':absolute_image_url,'business':business,'categories':categories, 'address':address,'all_ratings':all_ratings,'average_rating':average_rating,'total_rating':total_rating}) 



def view_product(request, bSlug, pSlug):
    product = Product.objects.filter(slug=pSlug).first()
    items= 0
    whishlist = 0
    if request.user.is_authenticated:
        items = get_cart_items(request.user)
        whishlist = get_wishlist_items(request.user)
    if product:
        all_ratings = BusinessRating.objects.filter(business=product.business)
        stars_list = [rating.stars for rating in all_ratings]

        if stars_list:
            average_rating = round(sum(stars_list) / len(stars_list), 1)
        else:
            average_rating = 0.0 
        total_rating = len(stars_list)
        markup_price = float(f'{product.price}') + (float(f'{product.price}') * 0.20)
        absolute_image_url = request.build_absolute_uri(product.image.url)
        absolute_page_url = request.build_absolute_uri()
        return render(request,'products/view_product.html',{'absolute_page_url':absolute_page_url,'absolute_image_url':absolute_image_url,'markup_price':markup_price,'product':product,'cart_items_count':items,"wishlist_items_count":whishlist,'average_rating':average_rating,'total_rating':total_rating})
    return render(request,'products/view_product.html')


def home(request):
    items = 0
    wishlist_items_count = 0
    if request.user.is_authenticated:
        items = get_cart_items(request.user)
        wishlist_items_count = get_wishlist_items(request.user)
    return render(request,'products/landing_page.html', {'cart_items_count': items, 'wishlist_items_count': wishlist_items_count})




from django.http import HttpResponse
from django.conf import settings
import os
from django.db.models import Q

def search_products(request):
    query = request.GET.get('q', '')
    products = []
    businesses = []

    if query:
        # Search products by name, description, or category
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query),
            status="active"
        ).select_related('business')[:20]  # Limit results

        # Search businesses by name or category
        businesses = BusinessInformation.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query),
            status="approved"
        )[:10]  # Limit results

    items = 0
    wishlist_items_count = 0
    if request.user.is_authenticated:
        items = get_cart_items(request.user)
        wishlist_items_count = get_wishlist_items(request.user)

    context = {
        'query': query,
        'products': products,
        'businesses': businesses,
        'cart_items_count': items,
        'wishlist_items_count': wishlist_items_count,
    }

    return render(request, 'products/search_results.html', context)

def robots_txt(request):
    file_path = os.path.join(settings.BASE_DIR, 'shop', 'static', 'robots.txt')
    with open(file_path, 'r') as f:
        content = f.read()

    return HttpResponse(content, content_type="text/plain")
