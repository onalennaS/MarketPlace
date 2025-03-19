from django.shortcuts import render, redirect
from .utils import login_required_custom, has_password
from allauth.socialaccount.models import SocialAccount
from .wrap_models.cart_models import Cart , Wishlist
def is_google_linked(user):
    try:
        social_account = SocialAccount.objects.get(user=user)
        return True
    except SocialAccount.DoesNotExist:
        return False

def is_verified(user):
    try:
        social_account = SocialAccount.objects.get(user=user)
        return True
    except SocialAccount.DoesNotExist:
        return False
# Create your views here.
# Create your views here.

def landing_page(request):
    return redirect('shop_base')
    return render(request, 'home/landing_page.html')


def home(request):
    return redirect('shop_base')
    return render(request, 'home/index.html')


def get_cart_items(user):
    return Cart.objects.filter(user=user).all().count()

def get_cart_total(cart_items):
    total = 0
    for item in cart_items:
        total += item.product.price
    return total

@login_required_custom
@has_password
def dash(request):
    return render(request, 'home/dash.html')

@login_required_custom
@has_password
def profile(request):
    return render(request, 'home/profile.html', {'linked':is_google_linked(request.user)})

@login_required_custom
def cart(request):
    items = get_cart_items(request.user)
    cart_items = Cart.objects.filter(user=request.user).all()
    price_total = get_cart_total(cart_items)
    return render(request, 'home/cart.html',{'cart_total':price_total,'cart_items':cart_items,'cart_items_count':items})

@login_required_custom
def wish_lists(request):
    items = get_cart_items(request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user).all()
    price_total = get_cart_total(wishlist_items)
    return render(request, 'home/wish_lists.html',{'wishlist_total':price_total,'wishlist_items':wishlist_items,'wishlist_items_count':items,"cart_items_count":get_cart_items(request.user)})

@login_required_custom
@has_password
def buyer_dashboard(request):
    return render(request, 'home/profile.html', {'linked':is_google_linked(request.user)})

@login_required_custom
@has_password
def address(request):

    return render(request, 'home/address.html')

@login_required_custom
def order_history(request):
    return render(request, 'home/order_history.html')

@login_required_custom
def view_order_details(request):
    return render(request, 'home/view_order_details.html')



@login_required_custom
def track_orders(request):
    return render(request, 'home/track_orders.html')

@login_required_custom
def buyer_reviews(request):
    return render(request, 'home/buyer_reviews.html')

@login_required_custom
def account_settings(request):
    return render(request, 'home/account_settings.html')

def buyer_support(request):
    return render(request, 'home/buyer_support.html')


@login_required_custom
def referrals_earnings(request):
    return render(request, 'home/referrals_earnings.html')

@login_required_custom
def gift_card(request):
    return render(request, 'home/gift_card.html')

@login_required_custom
def credit(request):
    return render(request, 'home/credit.html')



@login_required_custom
def checkout(request):
    return render(request, 'home/checkout.html')

@login_required_custom
def payment_history(request):
    return render(request, 'home/payment_history.html')

@login_required_custom
def subscription_plan(request):
    return render(request, 'home/subscription_plan.html')