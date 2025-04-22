from django.shortcuts import render, redirect
from django.http import JsonResponse
from seller.wrap_models.business_model import BusinessInformation, Moderation,Address
from .utils.business_transaction import withdraw_business_funds
from seller.wrap_models.orders_model import Order
from django.conf import settings
import requests
from .utils.business_transaction import transfer_money_to_business, clean_cart

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


from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return JsonResponse({"error": "No reference provided"}, status=400)

    # Verify transaction
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(verify_url, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]
        if data["status"] == "success":
            # Mark order as paid
            try:
                order = Order.objects.get(ref=reference)
                order.paid = True
                order.save()
                transaction = transfer_money_to_business(order.user,order.business,order,order.ref,"Success")
                clean_carts = clean_cart(order.user,order.business,order)
                return redirect("payment_successful",order.id)  # or render a success page
            except Order.DoesNotExist:
                return JsonResponse({"error": "Order not found"}, status=404)
        else:
            transaction = transfer_money_to_business(ref=reference,status="Failed")
            order = Order.objects.get(ref=reference)
            order.delete()
            return redirect("payment_failed") #redirect("payment_failed")
    else:
        transaction = transfer_money_to_business(ref=reference,status="Failed")
        order = Order.objects.get(ref=reference)
        order.delete()
        return redirect("payment_failed")

#@csrf_exempt
def paystack_webhook(request):
    secret = settings.PAYSTACK_SECRET_KEY
    paystack_signature = request.headers.get('x-paystack-signature')

    body = request.body
    expected_signature = hmac.new(
        key=bytes(secret, 'utf-8'),
        msg=body,
        digestmod=hashlib.sha512
    ).hexdigest()

    if paystack_signature != expected_signature:
        return HttpResponse(status=400)

    event = json.loads(body)

    if event["event"] == "charge.success":
        reference = event["data"]["reference"]
        # Find your order and mark it as paid
        try:
            order = Order.objects.get(ref=reference)
            order.paid = True
            order.save()
        except Order.DoesNotExist:
            pass
    elif event["event"] != "charge.success":
        try:
            order = Order.objects.get(ref=reference)
            order.paid = False
            order.save()
        except Order.DoesNotExist:
            pass
    return HttpResponse(status=200)

