from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from seller.utils.authentication_utils import login_required_custom, verify_role
import json
from seller.wrap_models.orders_model import Order
from seller.utils.send_emails import send_email_order_traking_update, send_email_order_delivered
from ..models import Courier, OrderDelivery
from transactions.utils.delivery_transactions import transfer_money_to_courier,withdraw_courier_funds
from transactions.models import DeliveryWallet, DeliveryTransaction
from ..utils import send_email_withdrawal
from user.wrap_models.cart_models import CartDeliveryAddress
# @login_required_custom
# @verify_role('business')
# def move_order_next_stage(request):

#     if not request.method == "POST":
#         return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

#     try:
#             data = json.loads(request.body)  # Parse JSON request body
#     except json.JSONDecodeError:
#         return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


#     order = Order.objects.filter(order_id=data.get('order_id')).first()
#     if order:
#         if order.status == "Pending":
#             order.status = "Processing"
#             send_email_order_traking_update(order)
#         elif order.status == "Processing":
#             order.status = "On route"
#             send_email_order_traking_update(order)
#         elif order.status == "On route":
#             # order.status = "Delivered"
#             # send_email_order_delivered(order)
#             return JsonResponse({'message':'action not allowed ', 'status':'error'},status=400)

#         else:
#             return JsonResponse({'message':'Something went wrong ', 'status':'error'},status=400)
#         order.save()
        
#     return JsonResponse({"message": f"Order #{order.order_id} moved to {order.status} stage",'status':'success'}, status=201)


@login_required_custom
@verify_role('courier')
def move_delivery_next_stage(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Request method not allowed'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON Data', 'status': 'error'}, status=400)

    order_id = data.get('order_id')
    new_status = data.get('new_status')
    codes = data.get('codes')

    if not order_id or not new_status:
        return JsonResponse({'message': 'Missing order_id or new_status', 'status': 'error'}, status=400)
    print(order_id)
    order_to_deliver = OrderDelivery.objects.filter(id=int(order_id)).first()
    
    if not order_to_deliver:
        return JsonResponse({'message': 'Order not found', 'status': 'error'}, status=404)

    if not order_to_deliver.is_taken:
        # When courier first accepts the order
        order_to_deliver.is_taken = True
        order_to_deliver.status = "waiting"
        order_to_deliver.user = request.user
    else:
        # Update based on new_status
        if new_status == "inprogress":
            if order_to_deliver.order.status == "Processing":
                return JsonResponse({'message': 'Package  is not ready for delivery', 'status': 'error'}, status=400)

            order_to_deliver.status = "inprogress"
        elif new_status == "completed" :
            if order_to_deliver.order.drop_codes != codes:
                return JsonResponse({'message': 'Invalid code provide, ask customer for correct code', 'status': 'error'}, status=400)

            order_to_deliver.status = "delivered"
            # Update main Order model as well
            if order_to_deliver.order:
                order = order_to_deliver.order
                order.status = "Delivered"
                order.save()
                send_email_order_delivered(order)
                transfer_money_to_courier(request.user,15,order.order_id)
        else:
            return JsonResponse({'message': 'Invalid status change', 'status': 'error'}, status=400)

    order_to_deliver.save()

    return JsonResponse({
        "message": f"Order #{order_to_deliver.order.order_id} moved to {order_to_deliver.status} stage",
        'status': 'success'
    }, status=201)




@login_required_custom
@verify_role('courier')
def rquest_withdraw(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Request method not allowed'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON Data', 'status': 'error'}, status=400)

    amount = data.get('amount')
    try:
    	amount=float(amount)
    	if amount < 10:
        	return JsonResponse({'message': 'amount withdrawable must be greater than R10', 'status': 'error'}, status=400)
    except Exception as e :
        return JsonResponse({'message': 'Invalid Request please contact help@onecartdiscovery.com', 'status': 'error'}, status=400)

    user = request.user

    trnsaction = withdraw_courier_funds(user,str(round(amount,2)))
    if trnsaction == None:
        return JsonResponse({'message': 'Amount requested is more than the available balance ', 'status': 'error'}, status=400)

    send_email_withdrawal(user,trnsaction)

    return JsonResponse({
        "message": f"withdrawal request sent successfully, you should revieve you amont in 2-3 business working days",
        'status': 'success'
    }, status=201)


@login_required_custom
@verify_role('courier')
def deliver_order(request, order_id):
    order_delivery = OrderDelivery.objects.filter(id=order_id, user=request.user).first()
    if not order_delivery:
        return render(request, 'courier/error.html', {'message': 'Order not found or not assigned to you.'})

    # Get delivery address coordinates
    delivery_address = CartDeliveryAddress.objects.filter(user=order_delivery.reciever, is_default=True).first()
    if not delivery_address or not delivery_address.latitude or not delivery_address.longitude:
        return render(request, 'courier/error.html', {'message': 'Delivery address coordinates not available.'})

    if request.method == 'POST':
        drop_code = request.POST.get('drop_code')
        if drop_code and len(drop_code) == 5 and drop_code.isdigit():
            if order_delivery.order.drop_codes == drop_code:
                # Mark as delivered
                order_delivery.status = 'Delivered'
                order_delivery.save()
                order_delivery.order.status = 'Delivered'
                order_delivery.order.save()
                return redirect('delivery_success')
            else:
                return JsonResponse({'message': 'Invalid drop code.', 'status': 'error'})
        else:
            return JsonResponse({'message': 'Please enter a valid 5-digit code.', 'status': 'error'})

    context = {
        'order_delivery': order_delivery,
        'delivery_address': delivery_address,
    }
    return render(request, 'courier/deliver.html', context)


@login_required_custom
@verify_role('courier')
def delivery_success(request):
    return render(request, 'courier/delivery_success.html')
