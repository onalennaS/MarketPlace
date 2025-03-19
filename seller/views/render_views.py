from django.shortcuts import render, redirect
from functools import wraps
from ..utils.authentication_utils import login_required_custom, has_password
from ..wrap_models.business_model import BusinessInformation, Moderation,Address
from ..wrap_models.product_model import Product, ProductModeration, RecentActivity, Extras,Addon
# Create your views here.
# Create your views here.

@login_required_custom
def dashboard(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    if business:
        return render(request, 'seller/new/dashboard.html', {'business':business})
    return render(request, 'seller/new/dashboard.html')

@login_required_custom
def business(request):
    businesses = BusinessInformation.objects.filter(owner=request.user.id).all()
    
    return render(request, 'seller/new/register_business.html',{'businesses':businesses})

@login_required_custom
def register_business_form(request):
    return render(request, 'seller/new/register_business_form.html')

@login_required_custom
def appeal_registration_view(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    address = Address.objects.filter(business=business).first()
    return render(request, 'seller/new/appeal_registration.html', {'business':business, 'address':address})

@login_required_custom
def business_status(request, business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    moderation = Moderation.objects.filter(business=business).first()
    return render(request, 'seller/new/businness_status.html',{'business':business, 'moderation':moderation})


@login_required_custom
def business_info(request):

    return render(request, 'seller/new/business_info.html')


@login_required_custom
def add_products(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    if business:
        return render(request, 'seller/new/add_products.html',{'business':business})
    return render(request, 'seller/new/add_products.html')

@login_required_custom
def manage_product(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    products = Product.objects.filter(business=business).all()
    activity = RecentActivity.objects.filter(business=business).all()
    extras = Extras.objects.filter(business=business).all()
    addons = Addon.objects.filter(business=business).all()
    if business:
        return render(request, 'seller/new/manage_product.html', {'addons':addons,'business':business, 'products':products, 'activities':activity, 'extras':extras})
    return redirect('business')

@login_required_custom
def edit_products(request,business_id,product_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    product = Product.objects.filter(id=int(product_id)).first()
    if business:
        return render(request, 'seller/new/edit_product.html',{'business':business, 'product':product})
    return render(request, 'seller/new/edit_product.html')

@login_required_custom
def view_product(request,product_id):
    product = Product.objects.filter(id=int(product_id)).first()
    moderation = ProductModeration.objects.filter(product=product).last()
    if product:
        return render(request, 'seller/new/view_product.html',{'moderation':moderation,'product':product})

    return render(request, 'seller/new/view_product.html')

@login_required_custom
def orders(request):
    return render(request, 'seller/new/orders.html')

@login_required_custom
def transaction(request):
    return render(request, 'seller/new/sales.html')

@login_required_custom
def customer(request):
    return render(request, 'seller/new/customer.html')

@login_required_custom
def settings(request):
    return render(request, 'seller/new/settings.html')

@login_required_custom
def invoice(request):
    return render(request, 'seller/new/invoice.html')

@login_required_custom
def report(request):
    return render(request, 'seller/new/report.html')



    #=============================
@login_required_custom
def order_tracking(request):
    return render(request, 'seller/order_tracking.html')


@login_required_custom
def pay_for_premium(request):
    return render(request, 'seller/pay_for_premium.html')

@login_required_custom
def reviews(request):
    return render(request, 'seller/reviews.html')

@login_required_custom
def view_stats(request):
    return render(request, 'seller/view_stats.html')

@has_password
def base(request):
    return render(request, 'seller/seller_profile.html')

@login_required_custom
@has_password
def user_profile(request):
    return render(request, 'seller/seller_profile.html')