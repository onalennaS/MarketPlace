from django.shortcuts import render
from django.http import JsonResponse
from seller.wrap_models.business_model import BusinessInformation, Moderation,Address
from .utils.business_transaction import withdraw_business_funds
# Create your views here.
import json
def business_withdrawal(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400) 

	business_id = int(data.get('business_id'))
	amount = float(data.get('amount'))
	business = BusinessInformation.objects.filter(id=business_id).first() 
	withdraw = withdraw_business_funds(business,amount)
	if not withdraw:
		return JsonResponse({'message':'Insuficient funds for withdrawal', "status":"error"}, status=400) 
	return JsonResponse({'message':"your withdrwal was successfully processed",'status':'success'},status=200)