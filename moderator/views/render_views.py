from django.shortcuts import render
from ..utils import login_required_custom
from seller.wrap_models.business_model import Moderation,BusinessInformation, Address
from seller.wrap_models.product_model import ProductModeration, Product

@login_required_custom
def dashboard(request):
	return render(request, 'moderator/dashboard.html')

@login_required_custom
def user(request):
	return render(request, 'moderator/user.html')

@login_required_custom
def business(request):
	moderations = Moderation.objects.all()
	all_business = moderations
	approved = [x for x in moderations if x.is_approved ==  True ]
	rejected = [x for x in moderations if x.is_rejected ==  True ]
	pending = [x for x in moderations if x.status ==  "pending" ]

	return render(request, 'moderator/business.html', {'moderations' : moderations,'approved':f'{len(approved)}', 'rejected':len(rejected), 'all_business':len(all_business), 'pending':len(pending)})

@login_required_custom
def view_business(request,business_id):
	business = BusinessInformation.objects.filter(id=int(business_id)).first()
	address = Address.objects.filter(business=business).first()
	return render(request, 'moderator/view_business.html', {'business' : business, 'address':address})


@login_required_custom
def notificatons(request):
	return render(request, 'moderator/notifications.html')

@login_required_custom
def settings(request):
	return None
	return render(request, 'moderator/settings.html')

@login_required_custom
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
def view_product_moderator(request,product_id):
    product = Product.objects.filter(id=int(product_id)).first()
    if product:
        return render(request, 'moderator/view_product.html',{'product':product})

    return render(request, 'moderator/view_product.html')