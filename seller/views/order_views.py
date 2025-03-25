from django.http import JsonResponse
from django.contrib.auth.models import User
from ..utils.authentication_utils import login_required_custom
import json 
from ..wrap_models.orders_model import Order
from ..utils.send_emails import send_email_order_traking_update, send_email_order_delivered


@login_required_custom
def move_order_next_stage(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
    except json.JSONDecodeError:
        return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

    print(data)
    order = Order.objects.filter(order_id=data.get('order_id')).first()
    if order:
        if order.status == "Pending":
            order.status = "Processing"
            send_email_order_traking_update(order)
        elif order.status == "Processing":
            order.status = "On route"
            send_email_order_traking_update(order)
        elif order.status == "On route":
            order.status = "Delivered"
            send_email_order_delivered(order)
        else:
            return JsonResponse({'message':'Something went wrong ', 'status':'error'},status=400)
        order.save()
        
    return JsonResponse({"message": f"Order #{order.order_id} moved to {order.status} stage",'status':'success'}, status=201)
