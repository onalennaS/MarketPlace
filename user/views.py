from django.shortcuts import render, redirect
from .utils import login_required_custom, has_password
from allauth.socialaccount.models import SocialAccount
from .wrap_models.cart_models import Cart , Wishlist,CartDeliveryMethod, CartDeliveryAddress, CartExtra
from seller.wrap_models.orders_model import Order, OrderItem, OrderExtra, OrderAddress
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
    cart_count = Cart.objects.filter(user=user).all().count() 
    items_in_cart_qty = Cart.objects.filter(user=user).all()
    cnt = 0
    for item in items_in_cart_qty:
        cnt += item.quantity
    return cnt

def get_extra_count(user):
    return CartExtra.objects.filter(user=user).all().count()

def get_order_items(order):
    return OrderItem.objects.filter(order=order).all().count()

def get_order_extra(order):
    return OrderExtra.objects.filter(order=order).all().count()

def get_cart_total(cart_items):
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity 
        
    return round(total,2)

def get_extra_total(extras):
    total = 0
    for extra in extras:
        total += float(extra.extra.price)
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
    extra_items = get_extra_count(request.user)
    cart_items = Cart.objects.filter(user=request.user).all()
    extras = CartExtra.objects.filter(user=request.user).all()
    item_total = get_cart_total(cart_items)
    extra_total = get_extra_total(extras)
    return render(request, 'home/cart.html',{'extra_total':extra_total,'extra_items':extra_items,'extras':extras,'cart_total':item_total,'cart_items':cart_items,'cart_items_count':items})

@login_required_custom
def wish_lists(request):
    items = get_cart_items(request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user).all()
    price_total = get_cart_total(wishlist_items)
    return render(request, 'home/wish_lists.html',{'wishlist_total':price_total,'wishlist_items':wishlist_items,'wishlist_items_count':items,"cart_items_count":get_cart_items(request.user)})

@login_required_custom
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).all()
    items = get_cart_items(request.user)
    method = None
    delivery_total = 0
    extras = CartExtra.objects.filter(user=request.user).all()
    delivery_method = CartDeliveryMethod.objects.filter(user=request.user).first()
    
    if delivery_method:
        if delivery_method.method == "pickup":
            method = "pickup"
        elif delivery_method.method == "delivery":
            method = "delivery"
            delivery_total = 15
        else:
            method = "None"

    delivery_address = CartDeliveryAddress.objects.filter(user=request.user).first()
    if not delivery_address:
        delivery_address = None

    extra_items = get_extra_count(request.user)
    price_total = get_cart_total(cart_items)
    extra_total = get_extra_total(extras)
    checkout_total = round(price_total + extra_total + delivery_total,2)
    return render(request, 'home/checkout.html', {'extra_total':extra_total,'extra_items':extra_items,'extras':extras,'delivery_address':delivery_address,'cart_items':cart_items,"cart_total":price_total,"items_count":items,"method":method,"checkout_total":checkout_total})

@login_required_custom
def payment_successful(request,order_id):
    order = Order.objects.filter(id=int(order_id)).first()
    return render(request, 'home/payment/payment_successful.html',{'order':order})

@login_required_custom
def payment_failed(request):
    return render(request, 'home/payment/payment_failed.html')

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
    orders = Order.objects.filter(user=request.user).all()
    
    return render(request, 'home/order_history.html',{'orders':orders})

@login_required_custom
def view_order_details(request,order_id):
    order = Order.objects.filter(id=int(order_id)).first()
    order_items = OrderItem.objects.filter(order=order).all()
    extras = OrderExtra.objects.filter(order=order).all()
    items_count = get_order_items(order)
    extra_count = get_order_extra(order) 
    price_total = get_cart_total(order_items)
    extra_total = get_extra_total(extras)
    delivery_total = 0
    if order.delivery_method == "delivery":
        delivery_total = 15
    total = price_total + extra_total + delivery_total 
    address = OrderAddress.objects.filter(order=order).first()
    return render(request, 'home/view_order_details.html',{"price_total":price_total,'extra_total':extra_total,'extras_count':extra_count,'items_count':items_count,'address':address,'extras':extras,'total':total,'order':order,'order_items':order_items})

@login_required_custom
def track_orders(request,order_id):
    order = Order.objects.filter(id=order_id).first()
    return render(request, 'home/track_orders.html',{'order':order})

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
def payment_history(request):
    return render(request, 'home/payment_history.html')

@login_required_custom
def subscription_plan(request):
    return render(request, 'home/subscription_plan.html')


@login_required_custom
def seller_landing_page(request):
   return render(request, 'seller/new/seller_landing_page.html')


