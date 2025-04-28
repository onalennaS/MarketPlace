from django.http import JsonResponse
from django.contrib.auth.models import User
from seller.utils.authentication_utils import login_required_custom, verify_role
import json 
from seller.wrap_models.orders_model import Order
from seller.utils.send_emails import send_email_order_traking_update, send_email_order_delivered
from ..models import Courier, OrderDelivery
from transactions.utils.delivery_transactions import transfer_money_to_courier

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
        elif new_status == "completed":
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


