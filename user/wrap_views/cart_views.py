from django.shortcuts import render, redirect
from ..utils import login_required_custom, has_password, send_email_order_confirmation
from seller.wrap_models.product_model import Product, Extras,Addon
from ..wrap_models.cart_models import Cart, CartExtra, Wishlist,CartAddons,CartDeliveryMethod,CartDeliveryAddress
from seller.wrap_models.orders_model import Order, OrderItem, OrderExtra, OrderAddons,OrderAddress
import json
from django.http import JsonResponse
from transactions.utils.business_transaction import transfer_money_to_business



@login_required_custom
def add_cart(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

	prodcut_id = int(data.get('product_id'))
	extras = data.get('extras')
	user = request.user

	if not prodcut_id:
		return JsonResponse({"message":"product does not exist", "status":"error"},status=404) 

	product = Product.objects.filter(id=prodcut_id).first()
	check_items = Cart.objects.filter(user=user).all()
	if len(check_items) > 0 :
		items = check_items.filter(product__business_in=[product]).all()
		if not len(items) > 0:
			return JsonResponse({"message":"Cannot add products from different businesses into the same cart", "status":"error"},status=404)
	cart_exists = Cart.objects.filter(product=product,user=user).all()
	if cart_exists:
		return JsonResponse({"message":"Product already added to cart", "status":"error"},status=404) 

	cart = Cart.objects.create(product=product,user=user)
	cart.save()
	
	if extras:
		for extra_id in extras.keys():
			extra = Addon.objects.filter(id=int(extra_id)).first()
			if extra:
				extra = CartAddons.objects.create(cart=cart,addon=extra)
				extra.save()
				
			else :
				print("no extra found")
	return JsonResponse({"message": "product added to cart successfully",'status':'success'}, status=201)
@login_required_custom


def add_extra_to_cart(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


	extras = data.get('extras')
	user = request.user

	
	if extras:
		for extra_id in extras.keys():
			extra = Extras.objects.filter(id=int(extra_id)).first()
			if extra:
				extra = CartExtra.objects.create(user=request.user,extra=extra)
				extra.save()
				
			else :
				print("no extra found")
	return JsonResponse({"message": "extras added to cart successfully",'status':'success'}, status=201)


@login_required_custom
def delete_extra(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

	extra_id = int(data.get('extra_id'))
	user = request.user

	if not extra_id:
		return JsonResponse({"message":"product does not exist", "status":"error"},status=404) 

	extra = CartExtra.objects.filter(id=extra_id).first()
	if extra:
		extra.delete()
	return JsonResponse({"message": f"item {extra.extra.name} removed from cart successfully",'status':'success'}, status=201)


@login_required_custom
def delete_cart(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

	prodcut_id = int(data.get('product_id'))
	user = request.user

	if not prodcut_id:
		return JsonResponse({"message":"product does not exist", "status":"error"},status=404) 

	cart = Cart.objects.filter(id=int(data['product_id'])).first()
	if cart:
		cart.delete()
	return JsonResponse({"message": f"item {cart.product.name} removed from cart successfully",'status':'success'}, status=201)


@login_required_custom
def add_wishlist(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

	prodcut_id = int(data.get('product_id'))

	if not prodcut_id:
		return JsonResponse({"message":"product does not exist", "status":"error"},status=404) 


	prodcut = Product.objects.filter(id=prodcut_id).first()
	wishlist_exists = Wishlist.objects.filter(product=prodcut,user=request.user).all()
	if wishlist_exists:
		return JsonResponse({"message":"Product already added to wishlist", "status":"error"},status=404) 
	wishlist = Wishlist.objects.create(product=prodcut,user=request.user)
	wishlist.save()

	return JsonResponse({"message": "product added to wishlist successfully",'status':'success'}, status=201)

@login_required_custom
def delete_wishlist(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

	prodcut_id = int(data.get('product_id'))
	user = request.user

	if not prodcut_id:
		return JsonResponse({"message":"product does not exist", "status":"error"},status=404) 

	wishlist = Wishlist.objects.filter(id=int(data['wishlist_id'])).first()
	if wishlist:
		wishlist.delete()
	return JsonResponse({"message": f"item {wishlist.product.name} removed from wishlist successfully",'status':'success'}, status=201)

@login_required_custom
def add_cart_delivery_method(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

	method = data.get('method')
	if not method:
		return JsonResponse({"message":"method is required", "status":"error"},status=404) 
	delivery_method = CartDeliveryMethod.objects.filter(user=request.user).first()
	if delivery_method:
		delivery_method.method = method
		delivery_method.save()
	else:
		delivery_method = CartDeliveryMethod.objects.create(method=method,user=request.user)
		delivery_method.save()

	return JsonResponse({"message": "Delivery method Updated successfully",'status':'success'}, status=201)

@login_required_custom
def add_cart_delivery_address(request):
	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
		data = json.loads(request.body)  # Parse JSON request body
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     

	address_type = data.get('address_type')
	if address_type == 'residential':
		house_no = data.get('house_no')
		street	= data.get('street')
		complex_name = data.get('complex_name')
		area = data.get('area')
		notes = data.get('notes')
		if not house_no:
			return JsonResponse({'message':'house number is required','status':'error'},status=404)

		if not street:
			return JsonResponse({'message':'street  is required','status':'error'},status=404)

		if not area:
			return JsonResponse({'message':' area is required','status':'error'},status=404)
	elif address_type == "campus" :
		instutition = data.get('instutition')
		block = data.get('block')
		venue = data.get('venue')
		notes = data.get('notes')
	
		if not instutition:
			return JsonResponse({'message':'instutition  is required','status':'error'},status=404)

		if not block:
			return JsonResponse({'message':'block  is required','status':'error'},status=404)

		if not venue:
			return JsonResponse({'message':' venue is required','status':'error'},status=404)
	else:
		return JsonResponse({'message':'no address selected', "status":"error"})



	address_exists = CartDeliveryAddress.objects.filter(user=request.user).first()
	if address_type == "residential":
		if address_exists:
			address_exists.address_type = "residential"
			address_exists.house_no = house_no
			address_exists.street = street
			address_exists.complex_name = complex_name
			address_exists.area = area
			address_exists.notes = notes
			address_exists.save()
		else:
			address = CartDeliveryAddress.objects.create(user=request.user,address_type=address_type, house_no=house_no, street=street,complex_name=complex_name,area=area, notes=notes)
			address.save()
	elif address_type == "campus":
		if address_exists:
			address_exists.address_type = "campus"
			address_exists.instutition = instutition
			address_exists.block = block
			address_exists.venue = venue
			address_exists.notes = notes
			address_exists.save()
		else:
			address = CartDeliveryAddress.objects.create(user=request.user,address_type=address_type, instutition=instutition, block=block,venue=venue,notes=notes)
			address.save()

	return JsonResponse({"message": "Delivery address Updated successfully",'status':'success'}, status=201)





@login_required_custom
def palce_order(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
    try:
            data = json.loads(request.body)  # Parse JSON request body

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)   


    cart_items = Cart.objects.filter(user=request.user).all()
    cart_extras = CartExtra.objects.filter(user=request.user).all()
    delivery_method = CartDeliveryMethod.objects.filter(user=request.user).first()
    if not delivery_method:
        return JsonResponse({'status':'error', 'message':'please choose a '}, status=403)
    
    address = CartDeliveryAddress.objects.filter(user=request.user).first()
    business = cart_items[0].product.business
    product_amount = 0
    extra_amount = 0 
    delivery_amount = 0 
    
    for item in cart_items:
        product_amount += int(item.product.price)
    for extra in cart_extras:
        extra_amount += int(extra.extra.price)

    
    if delivery_method.method == "delivery":
    	delivery_amount += 15

    total_amount = product_amount + extra_amount +delivery_amount
    
   
    order = Order.objects.create(business=business,user=request.user,total_amount=total_amount,delivery_method=delivery_method.method)
    order.save()

    send_email_order_confirmation(order,cart_extras,cart_items,total_amount)
    for item in cart_items:
        order_item = OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity)
        order_item.save()
        cart_addons = CartAddons.objects.filter(cart=item).all()
        if cart_addons:
            for addon in cart_addons:
                order_addon = OrderAddons.objects.create(product=order_item, addon=addon.addon)
                order_addon.save()
        item.delete()
    if cart_extras:
        for extra in cart_extras:
            order_extra = OrderExtra.objects.create(order=order,extra=extra.extra,quantity=extra.quantity)
            order_extra.save()
            extra.delete()
    if delivery_method.method == "delivery":
        if address.address_type == "residential":
            order_address = OrderAddress.objects.create(order=order,address_line_1=address.house_no, address_line_2=address.street,address_line_3=address.complex_name,address_line_4=address.area,notes=address.notes)
            order_address.save()
        elif address.address_type == "campus":
            order_address = OrderAddress.objects.create(order=order,address_line_1=address.instutition, address_line_2=address.block,address_line_3=address.venue,notes=address.notes)
            order_address.save()
        else:
            return JsonResponse({'message':'address not found ','status':'error'},status=404)

    transaction = transfer_money_to_business(request.user,order.business,total_amount,order)
    return JsonResponse({"message": "Order Placed Successfully successfully",'status':'success','order_id':order.id}, status=201)
    