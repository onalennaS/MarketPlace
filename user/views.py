from django.shortcuts import render, redirect
from django.urls import reverse
from .utils import login_required_custom
from seller.utils.authentication_utils import has_password
from allauth.socialaccount.models import SocialAccount
from .wrap_models.cart_models import Cart , Wishlist,CartDeliveryMethod, CartDeliveryAddress, CartExtra
from seller.wrap_models.orders_model import Order, OrderItem, OrderExtra, OrderAddress
from seller.wrap_models.business_model import BusinessRating, BusinessInformation, Address
from decimal import Decimal
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import LoginActivity, ReferralProfile,Referral

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
    if request.method == 'POST':
        if 'username' in request.POST:
            new_username = request.POST['username'].strip()
            if new_username != request.user.username:
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, 'Username is already taken.')
                    return redirect('dash')
            request.user.username = new_username
        if 'first_name' in request.POST:
            request.user.first_name = request.POST['first_name'].strip()
        if 'last_name' in request.POST:
            request.user.last_name = request.POST['last_name'].strip()
        if 'email' in request.POST:
            new_email = request.POST['email'].strip()
            if new_email != request.user.email:
                if User.objects.filter(email=new_email).exists():
                    messages.error(request, 'Email is already taken.')
                    return redirect('dash')
            request.user.email = new_email
        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('dash')
    return render(request, 'home/profile.html', {'is_google_linked': is_google_linked(request.user),'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
@has_password
def profile(request):
    if request.method == 'POST':
        if 'username' in request.POST:
            new_username = request.POST['username'].strip()
            if new_username != request.user.username:
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, 'Username is already taken.')
                    return redirect('profile')
            request.user.username = new_username
        if 'first_name' in request.POST:
            request.user.first_name = request.POST['first_name'].strip()
        if 'last_name' in request.POST:
            request.user.last_name = request.POST['last_name'].strip()
        if 'email' in request.POST:
            new_email = request.POST['email'].strip()
            if new_email != request.user.email:
                if User.objects.filter(email=new_email).exists():
                    messages.error(request, 'Email is already taken.')
                    return redirect('profile')
            request.user.email = new_email
        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'home/profile.html', {'is_google_linked': is_google_linked(request.user),'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

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

    ref_profile = ReferralProfile.objects.filter(user=request.user).first()
    free_delivery = "none"
    credit=None
    
    if delivery_method:
        if delivery_method.method == "pickup":
            method = "pickup"
        elif delivery_method.method == "delivery":
            if ref_profile:
                if ref_profile.wallet_balance > 11:
                    
                    delivery_total = 0
                    ref_profile.wallet_balance -= 12
                    free_delivery = 1
                elif ref_profile.wallet_balance >0:
                    free_delivery = 2
                    credit = ref_profile.wallet_balance
                    delivery_total += 12
                    delivery_total -= ref_profile.wallet_balance
                    ref_profile.wallet_balance = 0 
                else:
                    delivery_total += 12

                    
            method = "delivery"
             
        else:
            method = "None"

    delivery_address = CartDeliveryAddress.objects.filter(user=request.user,is_default=True).first()
    if not delivery_address:
        delivery_address = None

    extra_items = get_extra_count(request.user)
    price_total = get_cart_total(cart_items)
    extra_total = get_extra_total(extras)
    checkout_total = round(price_total + extra_total + delivery_total,2)
    discount = get_discount(cart_items)
    total_to_pay = Decimal(checkout_total)  - Decimal(discount)

    # Get list of business names with longitude and latitude coordinates
    businesses_with_coords = {}
    for cart_item in cart_items:
        business = cart_item.product.business
        address = Address.objects.filter(business=business).first()
        if address and address.latitude and address.longitude:
            businesses_with_coords = {
                'name': business.name,
                'longitude': float(address.longitude),
                'latitude': float(address.latitude)
            }
    print(businesses_with_coords)
    return render(request, 'home/checkout.html', {
        'discount':round(discount,2),
        'total_to_pay':total_to_pay,
        'cart_total':price_total,
        'extra_total':extra_total,
        'extra_items':extra_items,
        'extras':extras,
        'delivery_address':delivery_address,
        'cart_items':cart_items,
        'cart_items_count':items,'wishlist_items_count':wishlist_items_count,
        "items_count":items,
        "method":method,
        "checkout_total":checkout_total,
        'businesses_with_coords': businesses_with_coords,
        'credit':credit,
        'free_delivery': free_delivery,
        'delivery_total':delivery_total
    })

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
   
    return render(request, 'home/profile.html', {'linked':is_google_linked(request.user),'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
@has_password
def address(request):
   
    if request.method == 'POST':
        address_type = request.POST.get('address_type')
        action = request.POST.get('action')

        if action == 'delete':
            address_id = request.POST.get('address_id')
            try:
                address = CartDeliveryAddress.objects.get(id=address_id, user=request.user)
                address.delete()
                messages.success(request, 'Address deleted successfully.')
            except CartDeliveryAddress.DoesNotExist:
                messages.error(request, 'Address not found.')
            return redirect('address')

        elif action == 'set_default':
            address_id = request.POST.get('address_id')
            try:
                # First, unset all other addresses as default
                CartDeliveryAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
                # Then set the selected address as default
                address = CartDeliveryAddress.objects.get(id=address_id, user=request.user)
                address.is_default = True
                address.save()
                messages.success(request, 'Default address updated successfully.')
            except CartDeliveryAddress.DoesNotExist:
                messages.error(request, 'Address not found.')
            return redirect('address')

        # Validation for new address creation
        errors = []

        if not address_type or address_type not in ['residential', 'campus']:
            errors.append('Invalid address type.')

        phone = request.POST.get('phone', '').strip()
        if not phone:
            errors.append('Phone number is required.')
        elif not phone.isdigit() or len(phone) < 10:
            errors.append('Please enter a valid phone number (at least 10 digits).')

        if address_type == 'residential':
            house_no = request.POST.get('house_no', '').strip()
            street = request.POST.get('street', '').strip()
            area = request.POST.get('area', '').strip()
            latitude = request.POST.get('latitude', '').strip()
            longitude = request.POST.get('longitude', '').strip()

            if not house_no:
                errors.append('House number is required.')
            if not street:
                errors.append('Street is required.')
            if not area:
                errors.append('Area is required.')
            if not latitude or not longitude:
                errors.append('Location coordinates are required. Please select a location on the map.')

            print("---------",latitude,longitude)
            # Validate coordinates
            try:
                lat = float(latitude)
                lng = float(longitude)
                
            except ValueError:
                errors.append('Invalid coordinate format.')

        elif address_type == 'campus':
            institution = request.POST.get('institution', '').strip()
            block = request.POST.get('block', '').strip()
            venue = request.POST.get('venue', '').strip()
            latitude = request.POST.get('latitude', '').strip()
            longitude = request.POST.get('longitude', '').strip()

            if not institution:
                errors.append('Institution is required.')
            if not block:
                errors.append('Block is required.')
            if not venue:
                errors.append('Venue is required.')
            if not latitude or not longitude:
                errors.append('Location coordinates are required. Please select a location on the map.')

            # Validate coordinates
            try:
                lat = float(latitude)
                lng = float(longitude)
            except ValueError:
                errors.append('Invalid coordinate format.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('address')

        # Create address if validation passes
        if address_type == 'residential':
            CartDeliveryAddress.objects.create(
                user=request.user,
                address_type='residential',
                house_no=request.POST.get('house_no').strip(),
                street=request.POST.get('street').strip(),
                complex_name=request.POST.get('complex_name', '').strip() or None,
                area=request.POST.get('area').strip(),
                notes=request.POST.get('notes', '').strip() or None,
                latitude=request.POST.get('latitude').strip(),
                longitude=request.POST.get('longitude').strip(),
                phone=phone,
                is_default=True
            )
        elif address_type == 'campus':
            CartDeliveryAddress.objects.create(
                user=request.user,
                address_type='campus',
                instutition=request.POST.get('institution').strip(),
                block=request.POST.get('block').strip(),
                venue=request.POST.get('venue').strip(),
                latitude=request.POST.get('latitude').strip(),
                longitude=request.POST.get('longitude').strip(),
                phone=phone,
                is_default=True
            )

        messages.success(request, 'Address added successfully.')
        next_url = request.GET.get("next")
        if next_url and next_url != request.path:
            return redirect(next_url)
        return redirect('address')

    # Get existing addresses for display
    addresses = CartDeliveryAddress.objects.filter(user=request.user).order_by('-timestamp').all()
    return render(request, 'home/address.html', {'addresses': addresses,'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
def order_history(request):
    orders = Order.objects.filter(user=request.user).all()
    return render(request, 'home/order_history.html',{'orders':orders,'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

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
    address = CartDeliveryAddress.objects.filter(user=request.user).first()
    return render(request, 'home/view_order_details.html',{"price_total":price_total,'extra_total':extra_total,'extras_count':extra_count,'items_count':items_count,'address':address,'extras':extras,'total':total,'order':order,'order_items':order_items,'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
def track_orders(request,order_id):
    order = Order.objects.filter(id=order_id).first()
    if request.user == order.user:
        return render(request, 'home/track_orders.html',{'order':order,'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})
    return  render(request, 'home/errors/400.html')
@login_required_custom
def buyer_reviews(request):
    reviews = BusinessRating.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'home/buyer_reviews.html', {'reviews': reviews,'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
@has_password
def account_settings(request):
    if request.method == 'POST':
        if 'current_password' in request.POST and 'new_password' in request.POST and 'confirm_password' in request.POST:
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('account_settings')

            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return redirect('account_settings')

            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('account_settings')

            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('account_settings')

    # Get login activity data from LoginActivity model
    login_activity = LoginActivity.objects.filter(user=request.user).order_by('-login_time')[:10]

    # Convert to list of dicts for template compatibility
    login_activity_data = []
    for activity in login_activity:
        login_activity_data.append({
            'date_time': activity.login_time,
            'device': activity.device,
            'location': activity.location,
            'ip_address': activity.ip_address,
            'status': activity.status
        })

    return render(request, 'home/account_settings.html', {'login_activity': login_activity_data,'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
@has_password
def delete_account(request):
    if request.method == 'POST':
        # Delete all related data
        # Delete cart items
        Cart.objects.filter(user=request.user).delete()
        # Delete wishlist items
        Wishlist.objects.filter(user=request.user).delete()
        # Delete cart extras
        CartExtra.objects.filter(user=request.user).delete()
        # Delete delivery methods
        CartDeliveryMethod.objects.filter(user=request.user).delete()
        # Delete delivery addresses
        CartDeliveryAddress.objects.filter(user=request.user).delete()
        # Delete orders and related items
        orders = Order.objects.filter(user=request.user)
        for order in orders:
            OrderItem.objects.filter(order=order).delete()
            OrderExtra.objects.filter(order=order).delete()
        orders.delete()
        # Delete business ratings
        BusinessRating.objects.filter(user=request.user).delete()
        # Delete login activity
        LoginActivity.objects.filter(user=request.user).delete()
        # Delete social accounts
        SocialAccount.objects.filter(user=request.user).delete()
        # Finally delete the user
        request.user.delete()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')
    return redirect('account_settings')

def buyer_support(request):
    return render(request, 'home/buyer_support.html',{'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})


@login_required_custom
def referrals_earnings(request):
    profile = ReferralProfile.objects.filter(user=request.user).first()
    if profile:
        refs = Referral.objects.filter(referrer=request.user).all()

        return render(request, 'home/referrals_earnings.html',{'profile':profile,'refs':refs ,'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

    return render(request, 'home/referrals_earnings.html',{'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
def gift_card(request):
    return render(request, 'home/gift_card.html',{'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})

@login_required_custom
def credit(request):
    return render(request, 'home/credit.html',{'cart_items_count':get_cart_items(request.user),'wishlist_items_count':get_wishlist_items(request.user)})





@login_required_custom
def payment_history(request):
    from transactions.models import BusinessTransaction
    payments = BusinessTransaction.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'home/payment_history.html', {'payments': payments})

@login_required_custom
def subscription_plan(request):
    return render(request, 'home/subscription_plan.html')


@login_required_custom
def seller_landing_page(request):
    # Check if user is a customer (buyer)
    if request.user.groups.filter(name="customer").exists():
        messages.error(request, 'You need to sign in as a seller to access the seller page.')
        return redirect(reverse('signin') + '?seller_access=1')  # Redirect to signin page for buyers
    return render(request, 'seller/new/seller_landing_page.html')


def referral_page(request,code):
    if 'code' not in request.session:
        referrer = ReferralProfile.objects.filter(referral_code=code).first()
        referrer.view_clicks += 1
        referrer.save()
        request.session['code'] = referrer.referral_code
    return render(request, 'home/referrals_page.html')


