from django.shortcuts import render, redirect
from ..utils import login_required_custom, has_password
from seller.wrap_models.product_model import Product, Extras,Addon
from ..wrap_models.cart_models import Cart, CartExtra, Wishlist,CartAddons
import json
from django.http import JsonResponse



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
	cart_exists = Cart.objects.filter(product=product,user=user).all()
	if cart_exists:
		return JsonResponse({"message":"Product already added to cart", "status":"error"},status=404) 

	cart = Cart.objects.create(product=product,user=user)
	cart.save()
	print(extras)
	if extras:
		for extra_id in extras.keys():
			extra = Addon.objects.filter(id=int(extra_id)).first()
			if extra:
				extra = CartAddons.objects.create(cart=cart,addon=extra)
				extra.save()
				print(extra)
			else :
				print("no extra found")
	return JsonResponse({"message": "product added to cart successfully",'status':'success'}, status=201)

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
