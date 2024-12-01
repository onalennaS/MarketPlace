from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
def landing_page(request):
    return render(request, 'home/landing_page.html')

def home(request):
    return render(request, 'home/index.html')

def profile(request):
    return render(request, 'home/profile.html')

def buyer_dashboard(request):
    return render(request, 'home/profile.html')


def order_history(request):
    return render(request, 'home/order_history.html')

def wish_lists(request):
    return render(request, 'home/wish_lists.html')

def track_orders(request):
    return render(request, 'home/track_orders.html')

def buyer_reviews(request):
    return render(request, 'home/buyer_reviews.html')

def account_settings(request):
    return render(request, 'home/account_settings.html')

def buyer_support(request):
    return render(request, 'home/buyer_support.html')