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

from allauth.socialaccount.models import SocialAccount

def is_google_linked(user):
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
    
@login_required_custom
@has_password
def dash(request):
    return render(request, 'home/dash.html')

@login_required_custom
@has_password
def profile(request):
    return render(request, 'home/profile.html', {'linked':is_google_linked(request.user)})

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
def wish_lists(request):
    return render(request, 'home/wish_lists.html')

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
def cart(request):
    return render(request, 'home/cart.html')

@login_required_custom
def checkout(request):
    return render(request, 'home/checkout.html')

@login_required_custom
def payment_history(request):
    return render(request, 'home/payment_history.html')

@login_required_custom
def subscription_plan(request):
    return render(request, 'home/subscription_plan.html')