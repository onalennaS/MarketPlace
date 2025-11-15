from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from functools import wraps
from ..utils.authentication_utils import login_required_custom, has_password, verify_role
from ..wrap_models.business_model import BusinessInformation, Moderation,Address
from ..wrap_models.product_model import Product, ProductModeration, RecentActivity, Extras,Addon
from ..wrap_models.orders_model import Order, OrderItem, OrderExtra
from transactions.models import BusinessWallet, BusinessTransaction
from decimal import Decimal
from user.wrap_models.cart_models import CartDeliveryMethod, CartDeliveryAddress
from django.db.models import Count
from django.db.models import Avg
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Sum
from django.utils.dateformat import DateFormat
from datetime import datetime
# Create your views here.
# Create your views here.
def get_sales_data(trunc_func, business):
        return Order.objects.filter(paid=True, business=business) \
            .annotate(period=trunc_func('created_at')) \
            .values('period') \
            .annotate(total=Sum('total_amount')) \
            .order_by('period')

def process_data(queryset):
        labels = [entry['period'].strftime('%d %b') for entry in queryset]
        data = [float(entry['total']) for entry in queryset]
        return labels, data

@login_required_custom
@verify_role('business')
def dashboard(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id), owner=request.user).first()
    
    # Check if business exists and belongs to the user
    if not business:
        from django.contrib import messages
        messages.error(request, 'You do not have a registered business. Please register a business first.')
        from django.shortcuts import redirect
        return redirect('register_business_form')
    
    orders = Order.objects.filter(business=business).all()
    order_count = orders.count()
    recent_orders = orders.order_by('-created_at')[:4]
    total_customers = orders.values('user').distinct().count()
    try:
        average_paid_order_amount = round(orders.filter(paid=True).aggregate(avg_amount=Avg('total_amount'))['avg_amount'])
    except Exception as e:
        average_paid_order_amount = 0
        
    paid_order_count = orders.filter(paid=True).count()

    daily_sales = get_sales_data(TruncDay, business)
    weekly_sales = get_sales_data(TruncWeek, business)
    monthly_sales = get_sales_data(TruncMonth, business)

    daily_labels, daily_data = process_data(daily_sales)
    weekly_labels, weekly_data = process_data(weekly_sales)
    monthly_labels, monthly_data = process_data(monthly_sales)

    customers_by_month = (
        orders.annotate(month=TruncMonth('created_at'))  # Replace 'created_at' with your order date field
        .values('month')
        .annotate(count=Count('user', distinct=True))  # Count distinct users for each month
        .order_by('month')
    )

    labels = [DateFormat(entry['month']).format('M') for entry in customers_by_month]
    data = [entry['count'] for entry in customers_by_month]
   
    return render(request, 'seller/new/dashboard.html', {'business':business,
                                                            "order_count":order_count,
                                                            'total_customers':total_customers,
                                                            "average_paid_order_amount":average_paid_order_amount,
                                                            "transaction":paid_order_count,
                                                            "recent_orders":recent_orders,
                                                             'daily_labels': daily_labels,
                                                            'daily_data': daily_data,
                                                            'weekly_labels': weekly_labels,
                                                            'weekly_data': weekly_data,
                                                            'monthly_labels': monthly_labels,
                                                            'monthly_data': monthly_data,
                                                             'customer_labels': labels,
                                                            'customer_data': data,
                                                            })

@login_required_custom
@verify_role('business')
def business(request):
    businesses = BusinessInformation.objects.filter(owner=request.user.id).all()
    
    return render(request, 'seller/new/register_business.html',{'businesses':businesses})

@login_required_custom
@verify_role('business')
def register_business_form(request):
    return render(request, 'seller/new/register_business_form.html')

@login_required_custom
@verify_role('business')
def appeal_registration_view(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    address = Address.objects.filter(business=business).first()
    return render(request, 'seller/new/appeal_registration.html', {'business':business, 'address':address})

@login_required_custom
@verify_role('business')
def business_status(request, business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    moderation = Moderation.objects.filter(business=business).first()
    address = Address.objects.filter(business=business).first()
    return render(request, 'seller/new/businness_status.html',{'business':business, 'moderation':moderation, 'address':address})

@login_required_custom
@verify_role('business')
def business_info(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    return render(request, 'seller/new/business_info.html',{'business':business})

@login_required_custom
@verify_role('business')
def add_products(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    if business:
        return render(request, 'seller/new/add_products.html',{'business':business})
    return render(request, 'seller/new/add_products.html')

@login_required_custom
@verify_role('business')
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
@verify_role('business')
def edit_products(request,business_id,product_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    product = Product.objects.filter(id=int(product_id)).first()
    if business:
        return render(request, 'seller/new/edit_product.html',{'business':business, 'product':product})
    return render(request, 'seller/new/edit_product.html')

@login_required_custom
@verify_role('business')
def view_product(request,product_id):
    product = Product.objects.filter(id=int(product_id)).first()
    moderation = ProductModeration.objects.filter(product=product).last()
    if product:
        return render(request, 'seller/new/view_product.html',{'moderation':moderation,'product':product})

    return render(request, 'seller/new/view_product.html')

@login_required_custom
@verify_role('business')
def orders(request, business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    orders = Order.objects.filter(business=business).all()
    all_orders = []
    open_hour = datetime.strptime(business.open_time, "%H:%M").time()  # 8:00 AM
    close_hour = datetime.strptime(business.open_time, "%H:%M").time() 
    orders_open =  business.open_orders
    print(orders_open)
    for order in orders:
        if order.paid == True:
            delivery_method = CartDeliveryMethod.objects.filter(user=order.user).first()
            # if delivery_method:
            #     return render(request,"<h1> it works {delivery_method}</h>")
            if delivery_method.method == "delivery" :
                address = CartDeliveryAddress.objects.filter(user=order.user).first()
                message = address.notes
                method = 'Delivery'
                delivery = 15
            else:
                message = None
                method = 'Pickup'
                delivery = 0

            json_orders = {'items':[],'extras':[]}
            json_orders['id'] = f'{order.order_id}' 
            json_orders['message'] = f"{message}"
            json_orders['paymentStatus'] = "paid"
            json_orders['deliveryMethod'] = f'{method}'
            json_orders['timestamp'] = f'{order.created_at.strftime("%d %b %H:%M")}'
            json_orders['total'] = f'{float(order.total_price())}'
            json_orders['user'] = f'{order.user.username}'
            json_orders['recieved'] = f'{order.total_amount}'
            json_orders['delivery'] = f'{delivery}'
            if order.status == "Pending" :
                json_orders['status'] = "new"
            if order.status == "Processing":
                json_orders['status'] = "preparing"
            if order.status == "On route" :
                json_orders['status'] = "scheduled"
            if order.status == "Delivered":
                json_orders['status'] = "completed"

            order_items = OrderItem.objects.filter(order=order).all()
            extra_items = OrderExtra.objects.filter(order=order).all()
            for order_item in order_items:
                item = {
                    'product':order_item.product.name, 
                    'quantity': order_item.quantity,
                    'extras' : [ extra.addon.name for extra in order_item.CartAddon.all() ]
                        }
                json_orders['items'].append(item)

            for extra_item in extra_items:
                item = {'item':f'{extra_item.extra.name}'}
                json_orders['extras'].append(item)
           
            all_orders.append(json_orders)
        

    return render(request, 'seller/new/orders.html',{'business':business,'all_orders':all_orders,'open_hour':open_hour,'close_hour':close_hour,'orders_open':orders_open})

@login_required_custom
@verify_role('business')
def transaction(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    wallet = BusinessWallet.objects.filter(business=business).first()
    transactions = BusinessTransaction.objects.filter(receiver=business).all()
    trans_list = []
    for trans in transactions:
        data = {
            
            'ref':trans.ref,
            'customer':trans.sender.username,
            'transaction':trans.transaction_type,
            'amount': trans.amount,
            'status':trans.status,
            'date':trans.timestamp.strftime("%Y-%m-%d")

        }
        trans_list.append(data)
    trans_list.reverse()
    return render(request, 'seller/new/sales.html',{'count_transactions':transactions.count(),'business':business,'wallet':wallet,'transactions':trans_list})

@login_required_custom
@verify_role('business')
def customer(request, business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    if business:
        orders = Order.objects.filter(business=business).all()
        
        # Get all users who ordered
        user_orders = orders.values('user').annotate(order_count=Count('id'))
        
        customer_ids = [item['user'] for item in user_orders]
        total_customers = len(customer_ids)

        returning_customers = len([item for item in user_orders if item['order_count'] > 2])
        new_customers = total_customers - returning_customers

        # Get full user objects
        customers = User.objects.filter(id__in=customer_ids)
        customer_order_counts = {item['user']: item['order_count'] for item in user_orders}

        # Combine customer info + order count
        customers_with_orders = []
        for customer in customers:
            customers_with_orders.append({
                'user': customer,
                'order_count': customer_order_counts.get(customer.id, 0)
            })

        return render(request, 'seller/new/customer.html', {
            'business': business,
            'customers': customers_with_orders,
            'total_customers': total_customers,
            'returning_customers': returning_customers,
            'new_customers': new_customers
        })

    return render(request, 'seller/new/customer.html')


@login_required_custom
@verify_role('business')
def settings(request,business_id):
    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    return render(request, 'seller/new/settings.html',{'business':business})

@login_required_custom
@verify_role('business')
def invoice(request):
    return render(request, 'seller/new/invoice.html')


@login_required_custom
@verify_role('business')
def report(request,bussiness_id):
    business = BusinessInformation.objects.filter(id=bussiness_id).first()
    print(business)
    return render(request, 'seller/new/under_construction.html',{'business':business})



    #=============================
@verify_role('business')
@login_required_custom
def order_tracking(request):
    return render(request, 'seller/order_tracking.html')

@verify_role('business')
@login_required_custom
def pay_for_premium(request):
    return render(request, 'seller/pay_for_premium.html')

@verify_role('business')
@login_required_custom
def reviews(request):
    return render(request, 'seller/reviews.html')

@verify_role('business')
@login_required_custom
def view_stats(request):
    return render(request, 'seller/view_stats.html')

@verify_role('business')
@has_password
def base(request):
    return render(request, 'seller/seller_profile.html')


@login_required_custom
@has_password
def user_profile(request):
    return render(request, 'seller/seller_profile.html')