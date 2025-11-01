from django.shortcuts import render
from django.utils import timezone
from ..utils import login_required_custom
from seller.wrap_models.business_model import Moderation,BusinessInformation, Address
from seller.wrap_models.product_model import ProductModeration, Product
from seller.utils.authentication_utils import verify_role
from courier.models import Courier
from transactions.models import DeliveryTransaction

@login_required_custom
@verify_role(['admin','moderator'])
def dashboard(request):
    # Fetch business moderation data
    business_moderations = Moderation.objects.all()
    business_approved = business_moderations.filter(is_approved=True).count()
    business_rejected = business_moderations.filter(is_rejected=True).count()
    business_pending = business_moderations.filter(status="pending").count()

    # Fetch product moderation data
    product_moderations = ProductModeration.objects.all()
    product_approved = product_moderations.filter(is_approved=True).count()
    product_rejected = product_moderations.filter(is_rejected=True).count()
    product_pending = product_moderations.filter(status="pending").count()

    # Fetch user count
    from django.contrib.auth.models import User
    total_users = User.objects.count()

    # Fetch courier count
    courier_count = Courier.objects.count()

    # Comments count - assuming no comments model yet, set to 0 or implement if exists
    comments_total = 0  # Placeholder, update if comments model is available
    comments_reviewed = 0
    comments_pending = 0

    # Dynamic notifications based on pending items
    notifications = []
    if business_pending > 0:
        notifications.append({
            'type': 'business',
            'message': f'{business_pending} business(es) pending approval',
            'action': 'Review Businesses'
        })
    if product_pending > 0:
        notifications.append({
            'type': 'product',
            'message': f'{product_pending} product(s) pending approval',
            'action': 'Review Products'
        })

    # Chart data - Aggregate user and business growth by month (last 6 months)
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    import datetime

    # User growth
    six_months_ago = timezone.now() - datetime.timedelta(days=180)
    user_growth = User.objects.filter(date_joined__gte=six_months_ago).annotate(
        month=TruncMonth('date_joined')
    ).values('month').annotate(count=Count('id')).order_by('month')

    # Business growth
    business_growth = BusinessInformation.objects.filter(date_created__gte=six_months_ago).annotate(
        month=TruncMonth('date_created')
    ).values('month').annotate(count=Count('id')).order_by('month')

    # Prepare chart data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    user_counts = [0] * 6
    business_counts = [0] * 6

    current_year = timezone.now().year
    for i, month in enumerate(months):
        month_date = datetime.date(current_year, i+1, 1)
        for ug in user_growth:
            if ug['month'].month == i+1:
                user_counts[i] = ug['count']
        for bg in business_growth:
            if bg['month'].month == i+1:
                business_counts[i] = bg['count']

    # Sales trend - placeholder, as no sales model is evident; set to static or implement if exists
    sales_data = [1000, 2000, 3500, 5000, 7000, 9000]  # Static for now

    context = {
        'business_approved': business_approved,
        'business_rejected': business_rejected,
        'business_pending': business_pending,
        'product_approved': product_approved,
        'product_rejected': product_rejected,
        'product_pending': product_pending,
        'total_users': total_users,
        'courier_count': courier_count,
        'comments_total': comments_total,
        'comments_reviewed': comments_reviewed,
        'comments_pending': comments_pending,
        'notifications': notifications,
        'months': months,
        'user_counts': user_counts,
        'business_counts': business_counts,
        'sales_data': sales_data,
    }

    return render(request, 'moderator/dashboard.html', context)

@login_required_custom
@verify_role(['admin','moderator'])
def user(request):
	return render(request, 'moderator/user.html')

@login_required_custom
@verify_role(['admin','moderator'])
def business(request):
	moderations = Moderation.objects.all()
	all_business = moderations
	approved = [x for x in moderations if x.is_approved ==  True ]
	rejected = [x for x in moderations if x.is_rejected ==  True ]
	pending = [x for x in moderations if x.status ==  "pending" ]

	return render(request, 'moderator/business.html', {'moderations' : moderations,'approved':f'{len(approved)}', 'rejected':len(rejected), 'all_business':len(all_business), 'pending':len(pending)})

@login_required_custom
@verify_role(['admin','moderator'])
def view_business(request,business_id):
	business = BusinessInformation.objects.filter(id=int(business_id)).first()
	address = Address.objects.filter(business=business).first()
	return render(request, 'moderator/view_business.html', {'business' : business, 'address':address})

@login_required_custom
@verify_role(['admin','moderator'])
def notificatons(request):
	return render(request, 'moderator/notifications.html')

@login_required_custom
@verify_role(['admin','moderator'])
def settings(request):
	return None
	return render(request, 'moderator/settings.html')

@login_required_custom
@verify_role(['admin','moderator'])
def product(request):
	moderations = ProductModeration.objects.all()
	products = moderations
	approved = [x for x in products if x.is_approved ==  True ]
	rejected = [x for x in products if x.is_rejected ==  True ]
	pending = [x for x in products if x.status ==  "pending" ]
	moderation = ProductModeration.objects.all()
	for product in products:
		print(product.product, product.product.business.name,product.product.status)
	return render(request, 'moderator/product.html', {'moderations':moderation,'products' : moderations,'approved':f'{len(approved)}', 'rejected':len(rejected), 'all_products':len(products), 'pending':len(pending)})

@login_required_custom
@verify_role(['admin','moderator'])
def view_product_moderator(request,product_id):
    product = Product.objects.filter(id=int(product_id)).first()
    if product:
        return render(request, 'moderator/view_product.html',{'product':product})

    return render(request, 'moderator/view_product.html')

@login_required_custom
@verify_role(['admin','moderator'])
def courier(request):
	all_courier = Courier.objects.all()
	return render(request, 'moderator/courier.html',{'all_courier':all_courier,'count_courier':len(all_courier)})

@login_required_custom
@verify_role(['admin','moderator'])
def view_courier(request,courier_id):
	courier = Courier.objects.filter(id=int(courier_id)).first()
	return render(request, 'moderator/view_courier.html', {'courier' : courier})

	

@login_required_custom
@verify_role(['admin','moderator'])
def payout(request):
	delivery_transactions = DeliveryTransaction.objects.filter(transaction_type="Withdrawal").all()
	return render(request, 'moderator/courier_payment.html', {'delivery_transactions' : delivery_transactions})

