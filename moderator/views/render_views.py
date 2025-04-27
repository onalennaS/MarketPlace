from django.shortcuts import render
from ..utils import login_required_custom
from seller.wrap_models.business_model import Moderation,BusinessInformation, Address
from seller.wrap_models.product_model import ProductModeration, Product
from seller.utils.authentication_utils import verify_role
from courier.models import Courier

@login_required_custom
@verify_role(['admin','moderator'])
def dashboard(request):
	return render(request, 'moderator/dashboard.html')

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

	