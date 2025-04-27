
from django.shortcuts import render
from ..utils import login_required_custom
from seller.wrap_models.business_model import Moderation,BusinessInformation
from seller.utils.send_emails import send_email_reject, send_email_approve
import json 
from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from seller.utils.authentication_utils import verify_role
from courier.models import Courier

@login_required_custom
@verify_role(['admin','moderator'])
def approve_business(request):

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
	business.status = "approved"
	business.save()
	moderation.is_reviewed = True
	moderation.status = "approved"
	moderation.is_approved = True 
	moderation.save()
	group = Group.objects.filter(name="business").first()
	user = User.objects.filter(id=business.owner.id).first()
	if group and user:
		user.groups.add(group)
		user.save()
	send_email_approve(business)
	return JsonResponse({"message": "business reviewed successfully ",'status':'success'}, status=201)

@login_required_custom
@verify_role(['admin','moderator'])
def reject_business(request):

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

	 

	business.status = "rejected"
	business.save()
	moderation.is_reviewed = True
	moderation.status = "rejected"
	moderation.is_rejected = False 
	moderation.reason = data.get('reason')
	send_email_reject(business)
	moderation.save()
	return JsonResponse({"message": "business reviewed successfully ",'status':'success'}, status=201)

@login_required_custom
@verify_role(['admin','moderator'])
def ban_business(request):

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



@login_required_custom
@verify_role(['admin','moderator'])
def approve_courier(request):

	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'status':'error', 'message':'Invalid json data'}, status=400)     

	courier_id = data.get('courier_id')

	courier = Courier.objects.filter(id=int(courier_id)).first()
	if not courier:
		return JsonResponse({'status':'error', 'message':'Courier not found'}, status=400)     


	if courier.is_reviewed == True:
		return JsonResponse({'status':'error', 'message':'Courier already reviewd'}, status=400)     
	courier.status = "approved"
	courier.is_reviewed = True
	courier.save()
	# group = Group.objects.filter(name="Courier").first()
	# user = User.objects.filter(id=Courier.owner.id).first()
	# if group and user:
	# 	user.groups.add(group)
	# 	user.save()
	# send_email_approve(Courier)
	return JsonResponse({"message": "Courier reviewed successfully ",'status':'success'}, status=201)

@login_required_custom
@verify_role(['admin','moderator'])
def reject_courier(request):

	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'status':'error', 'message':'Invalid json data'}, status=400)     

	courier_id = data.get('courier_id')

	courier = Courier.objects.filter(id=int(courier_id)).first()
	if not courier:
		return JsonResponse({'status':'error', 'message':'Courier not found'}, status=400)     


	if courier.is_reviewed == True:
		return JsonResponse({'status':'error', 'message':'Courier already reviewd'}, status=400)     
	courier.status = "rejected"
	courier.is_reviewed = True
	courier.save()
	# group = Group.objects.filter(name="business").first()
	# user = User.objects.filter(id=business.owner.id).first()
	# if group and user:
	# 	user.groups.add(group)
	# 	user.save()
	# send_email_approve(business)
	return JsonResponse({"message": "Courier reviewed successfully ",'status':'success'}, status=201)