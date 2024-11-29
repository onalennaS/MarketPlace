from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
def base(request):
    return render(request, 'seller/seller_profile.html')



def user_profile(request):

    return render(request, 'seller/seller_profile.html')

def business_info(request):
    
    return render(request, 'seller/business_info.html')

def view_stats(request):
   
    return render(request, 'seller/view_stats.html')

def add_products(request):
   
    return render(request, 'seller/add_products.html')

def edit_products(request):
   
    return render(request, 'seller/edit_products.html')

def orders(request):
    
    return render(request, 'seller/orders.html')

def order_tracking(request):
    
    return render(request, 'seller/order_tracking.html')

def transaction(request):
   
    return render(request, 'seller/transaction.html')

def pay_for_premium(request):
    
    return render(request, 'seller/pay_for_premium.html')


