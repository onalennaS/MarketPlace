from django.shortcuts import render, redirect
from .utils import login_required_custom, has_password
from allauth.socialaccount.models import SocialAccount
from .wrap_models.cart_models import Cart , Wishlist,CartDeliveryMethod, CartDeliveryAddress, CartExtra
from seller.wrap_models.orders_model import Order, OrderItem, OrderExtra, OrderAddress
from seller.wrap_models.business_model import BusinessRating
from decimal import Decimal
from django.http import HttpResponse

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

from user.wrap_models.cart_models import Cart, Wishlist
from django.http import HttpResponse




def get_wishlist_items(user):
    return Wishlist.objects.filter(user=user).all().count()

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
        try:
            total += item.product.price * item.quantity 
        except Exception as e:
            total += item.product.price
    return round(total,2)

def get_extra_total(extras):
    total = 0
    for extra in extras:
        total += extra.extra.price
    return total


def get_discount(cart_items):
    discount_factor = 0
    for item in cart_items:
        discount_factor += item.quantity
    discount = 4
    discounted_amount = 0
    if discount_factor == 3 :
        discounted_amount = Decimal(discount) * Decimal(1)
    elif discount_factor >3 and discount_factor < 6 :
        discounted_amount = Decimal(discount) * Decimal(1.5)
    elif discount_factor > 5 and discount_factor < 8:
        discounted_amount = discount * 3
    return Decimal(discounted_amount)

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
    wishlist_items_count = get_wishlist_items(request.user)
    extra_items = get_extra_count(request.user)
    cart_items = Cart.objects.filter(user=request.user).all()
    extras = CartExtra.objects.filter(user=request.user).all()
    item_total = get_cart_total(cart_items)
    extra_total = get_extra_total(extras)
    has_out_of_stock_item = False 
    for item in cart_items:
        if item.product.quantity < 1 :
            has_out_of_stock_item = True
            break
    return render(request, 'home/cart.html',{'extra_total':extra_total,'extra_items':extra_items,'extras':extras,'cart_total':item_total,'cart_items':cart_items,'cart_items_count':items,'wishlist_items_count':wishlist_items_count,'has_out_of_stock_item':has_out_of_stock_item})

@login_required_custom
def wish_lists(request):
    items = get_cart_items(request.user)
    wishlist_items_count = get_wishlist_items(request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user).all()
    price_total = get_cart_total(wishlist_items)
    return render(request, 'home/wish_lists.html',{'wishlist_total':price_total,'wishlist_items':wishlist_items,'wishlist_items_count':wishlist_items_count,"cart_items_count":items})

@login_required_custom
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).all()
    items = get_cart_items(request.user)
    wishlist_items_count = get_wishlist_items(request.user)
    
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
    discount = get_discount(cart_items)
    total_to_pay = Decimal(checkout_total)  - Decimal(discount)
    return render(request, 'home/checkout.html', {'discount':round(discount,2),'total_to_pay':total_to_pay,'extra_total':extra_total,'extra_items':extra_items,'extras':extras,'delivery_address':delivery_address,'cart_items':cart_items,"cart_total":price_total,"items_count":items,"method":method,"checkout_total":checkout_total})

@login_required_custom
def payment_successful(request,order_id):
    order = Order.objects.filter(id=int(order_id)).first()
    business_ratings = BusinessRating.objects.filter(user=request.user,business=order.business).first()
    rated = False
    if business_ratings:
        rated = True 
    return render(request, 'home/payment/payment_successful.html',{'order':order,'rated':rated})

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
    if request.user != order.user:
        return  render(request, 'home/errors/400.html')
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
    if request.user == order.user:
        return render(request, 'home/track_orders.html',{'order':order})
    return  render(request, 'home/errors/400.html')
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


