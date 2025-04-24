from django.http import JsonResponse
from django.contrib.auth.models import User
from ..utils.authentication_utils import login_required_custom, verify_role
import json 
from ..wrap_models.orders_model import Order
from ..utils.send_emails import send_email_order_traking_update, send_email_order_delivered
from ..wrap_models.business_model import BusinessInformation

@login_required_custom
@verify_role('business')
def move_order_next_stage(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
    except json.JSONDecodeError:
        return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


    order = Order.objects.filter(order_id=data.get('order_id')).first()
    if order:
        if order.status == "Pending":
            order.status = "Processing"
            send_email_order_traking_update(order)
        elif order.status == "Processing":
            order.status = "On route"
            send_email_order_traking_update(order)
        elif order.status == "On route":
            # order.status = "Delivered"
            # send_email_order_delivered(order)
            return JsonResponse({'message':'action not allowed ', 'status':'error'},status=400)

        else:
            return JsonResponse({'message':'Something went wrong ', 'status':'error'},status=400)
        order.save()
        
    return JsonResponse({"message": f"Order #{order.order_id} moved to {order.status} stage",'status':'success'}, status=201)

@login_required_custom
@verify_role('business')
def start_order(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
    except json.JSONDecodeError:
        return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


    business = BusinessInformation.objects.filter(id=data.get('business_id')).first()
    status = data.get('status')
    if not business:
        return JsonResponse({'message':'business not found', "status":"error"}, status=400)     
        
    if status != "start":
        return JsonResponse({'message':'Invalid action ', "status":"error"}, status=400)     
    print(business)
    print(status)
    print(business.open_orders)
    print("***************************")
    business.open_orders = True 
    business.save()
    print(business.open_orders)

    return JsonResponse({"message": f"Store is now open for orders",'status':'success'}, status=201)


@login_required_custom
@verify_role('business')
def stop_order(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
    except json.JSONDecodeError:
        return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


    business = BusinessInformation.objects.filter(id=data.get('business_id')).first()
    status = data.get('status')
    if not business:
        return JsonResponse({'message':'business not found', "status":"error"}, status=400)     
        
    if status != "stop":
        return JsonResponse({'message':'Invalid action ', "status":"error"}, status=400)     

    business.open_orders = False 
    business.save()
    return JsonResponse({"message": f"Store is now closed",'status':'success'}, status=201)
