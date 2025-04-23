from django.shortcuts import render
from ..utils import login_required_custom, send_email_approve_to_user,send_email_reject_to_user
from seller.wrap_models.business_model import Moderation,BusinessInformation
from seller.wrap_models.product_model import ProductModeration, Product
from seller.utils.authentication_utils import verify_role

import json 
from django.http import JsonResponse

@login_required_custom
@verify_role(['admin','moderator'])
def approve_product(request):

	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'status':'error', 'message':'Invalid json data'}, status=400)     

	product_id = data.get('product_id')

	product = Product.objects.filter(id=int(product_id)).first()
	if not product:
		return JsonResponse({'status':'error', 'message':'product not found'}, status=400)     

	moderation = ProductModeration.objects.filter(product=product).first()
	if not moderation:
		return JsonResponse({'status':'error', 'message':'product is invalid'}, status=400)     

	if moderation.is_reviewed == True:
		return JsonResponse({'status':'error', 'message':'product already reviewd'}, status=400)     

	product.status = "active"
	product.save()
	moderation.is_reviewed = True
	moderation.status = "approved"
	moderation.is_approved = True 
	moderation.save()
	send_email_approve_to_user(product)
	return JsonResponse({"message": "business reviewed successfully ",'status':'success'}, status=201)

@login_required_custom
@verify_role(['admin','moderator'])
def reject_product(request):

	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'status':'error', 'message':'Invalid json data'}, status=400)     

	product_id = data.get('product_id')

	product = Product.objects.filter(id=int(product_id)).first()
	if not product:
		return JsonResponse({'status':'error', 'message':'product not found'}, status=400)     

	moderation = ProductModeration.objects.filter(product=product).first()
	if not moderation:
		return JsonResponse({'status':'error', 'message':'product is invalid'}, status=400)     

	 

	product.status = "rejected"
	product.save()
	moderation.is_reviewed = True
	moderation.status = "rejected"
	moderation.is_rejected = True 
	moderation.reason = data.get('reason')
	moderation.save()
	send_email_reject_to_user(product)
	return JsonResponse({"message": "product reviewed successfully ",'status':'success'}, status=201)

@login_required_custom
@verify_role(['admin','moderator'])
def deactivate_product(request):

	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'status':'error', 'message':'Invalid json data'}, status=400)     

	business_id = data.get('business_id')

	business = BusinessInformation.objects.filter(id=int(business_id)).first()
	if not business:
		return JsonResponse({'status':'error', 'message':'business not found'}, status=400)     

	moderation = Moderation.objects.filter(business=business).first()
	if not moderation:
		return JsonResponse({'status':'error', 'message':'business is invalid'}, status=400)     

	if moderation.is_reviewed == True:
		return JsonResponse({'status':'error', 'message':'business already reviewd'}, status=400)     

	business.status == "banned"
	business.save()
	moderation.is_reviewed = True
	moderation.status = "banned"
	moderation.reason = data.get('reason') 
	moderation.save()
	return JsonResponse({"message": "business reviewed successfully ",'status':'success'}, status=201)
