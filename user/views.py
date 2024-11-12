from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
def landing_page(request):
    return render(request, 'home/landing_page.html')

def home(request):
    return render(request, 'home/index.html')

def seller_dashboard(request):
    return render(request, 'home/seller_profile.html')

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    return render(request, 'home/seller_profile.html')

def business_info(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/business_info.html')

def view_stats(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/view_stats.html')

def add_products(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/add_products.html')

def edit_products(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/edit_products.html')

def orders(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/orders.html')

def order_tracking(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/order_tracking.html')

def transaction(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/transaction.html')

def pay_for_premium(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home/pay_for_premium.html')

