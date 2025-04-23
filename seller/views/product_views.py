from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..utils.authentication_utils import login_required_custom, has_password, verify_role
#from ..utils.send_emails import 
from ..utils.product_validation import validate_business_data
import json 
from ..wrap_models.business_model import BusinessInformation, Address, Moderation
from ..wrap_models.product_model import Product, ProductModeration, RecentActivity, Extras,Addon
from moderator.utils import send_email_pending_to_user


from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

@csrf_exempt  # Only use if CSRF protection is causing issues
@login_required_custom
@verify_role('business')
def add_product(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Request method not allowed'}, status=403)

    try:
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = float(request.POST.get('price')) + float(4)
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        small_description = request.POST.get('small_description')
        business_id = request.POST.get('business_id')

        # Get the business instance
        business = BusinessInformation.objects.filter(id=business_id).first()
        if not business:
            return JsonResponse({'status': 'error', 'message': 'Business not found'}, status=404)

        # Check if the product already exists
        if Product.objects.filter(business=business, name=name).exists():
            return JsonResponse({'status': 'error', 'message': 'Product already exists'}, status=400)

        # Handle file upload
        image = request.FILES.get('image')  # Image from the request

        # Validate image file
        if image and not image.content_type.startswith('image/'):
            return JsonResponse({'status': 'error', 'message': 'Invalid file type. Only images allowed'}, status=400)

        # Create Product
        product = Product.objects.create(
            business=business,
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            description=description,
            small_description=small_description,
            image=image  # Store uploaded image
        )

        # Create moderation and activity logs
        moderator = User.objects.filter(email="sixskies25@gmail.com").first()
        moderation = ProductModeration.objects.create(product=product, moderator=moderator)
        activity = RecentActivity.objects.create(business=business, product=product, activity="Added")

        # Save all objects
        product.save()
        moderation.save()
        activity.save()

        # Notify the user
        send_email_pending_to_user(product)

        return JsonResponse({"message": "Product added successfully", 'status': 'success'}, status=201)

    except ValidationError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

    except Exception as e:
        return JsonResponse({"status": "error", "message": "An unexpected error occurred", "details": str(e)}, status=500)

@login_required_custom
@verify_role('business')
def delete_product(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)   

    product = Product.objects.filter(id=int(data['product_id'])).first()
    if product:
        business = product.business
        activity = RecentActivity.objects.create(business=business, product=product, activity="Deleted")
        activity.save()
        product.delete()	
        return JsonResponse({"message": "product deleted successfully",'status':'success'}, status=201)
    return JsonResponse({'status':'error', 'message':'product not found'}, status=403)


@login_required_custom
@verify_role('business')
def edit_product(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
            

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)    


    product = Product.objects.filter(id=int(data['product_id'])).first()
    if product:

        product.name = data.get('name')
        product.category = data.get('category')
        product.price = float(data.get('price')) + float(4)
        product.quantity = data.get('quantity')
        product.description = data.get('description')
        product.small_description = data.get('small_description')
        business = product.business
        activity = RecentActivity.objects.create(business=business, product=product, activity="Updated")
        activity.save()
        product.save()
        return JsonResponse({"message": "product added successfully",'status':'success'}, status=201)
    return JsonResponse({"message": "product Not found",'status':'error'}, status=201)


@login_required_custom
@verify_role('business')
def activate_product(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
            errors = validate_business_data(data)
            if errors:
                return JsonResponse({"status":"error","message":f"{errors}"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)     
    return JsonResponse({"message": "product added successfully",'status':'success'}, status=201)

@login_required_custom
@verify_role('business')
def deactivate_product(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
            errors = validate_business_data(data)
            if errors:
                return JsonResponse({"status":"error","message":f"{errors}"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)     
    return JsonResponse({"message": "product added successfully",'status':'success'}, status=201)

@login_required_custom
@verify_role('business')
def add_extras(request):

	if not request.method == "POST":
		return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

	try:
			data = json.loads(request.body)  # Parse JSON request body
			
	except json.JSONDecodeError:
		return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


	business = int(data.get('business_id'))
	business = BusinessInformation.objects.filter(id=business).first()
	name = data.get('name')
	
	price = float(data.get('price')) + float(0.55)

	extras_exists = Extras.objects.filter(business=business, name=name ).first()
	if extras_exists:
		return JsonResponse({'message':f'Extras {name} already exists', "status":"error"}, status=400) 

	extras = Extras.objects.create(business=business, name=name,  price=price)
	extras.save()
	
	return JsonResponse({"message": f"Extras {name} added successfully",'status':'success'}, status=201)

@login_required_custom
@verify_role('business')
def delete_extras(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)   

    extra = Extras.objects.filter(id=int(data['extra_id'])).first()
    if extra:
        extra.delete()	
        return JsonResponse({"message": f"Extra {extra.name} deleted successfully",'status':'success'}, status=201)
    return JsonResponse({'status':'error', 'message':'product not found'}, status=403)

@login_required_custom
@verify_role('business')
def add_addons(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
            
    except json.JSONDecodeError:
        return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


    business = int(data.get('business_id'))
    business = BusinessInformation.objects.filter(id=business).first()
    name = data.get('name')
    

    addon_exists = Addon.objects.filter(business=business, name=name ).first()
    if addon_exists:
        return JsonResponse({'message':f'Add-On {name} already exists', "status":"error"}, status=400) 

    addon = Addon.objects.create(business=business, name=name)
    addon.save()
    
    return JsonResponse({"message": f"Add-On {name} added successfully",'status':'success'}, status=201)

@login_required_custom
@verify_role('business')
def delete_addon(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
            data = json.loads(request.body)  # Parse JSON request body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)   

    addon = Addon.objects.filter(id=int(data['addon_id'])).first()
    if addon:
        addon.delete()  
        return JsonResponse({"message": f"addon {addon.name} deleted successfully",'status':'success'}, status=201)
    return JsonResponse({'status':'error', 'message':'product not found'}, status=403)