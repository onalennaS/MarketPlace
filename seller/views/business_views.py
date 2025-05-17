from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from functools import wraps
from ..utils.authentication_utils import login_required_custom, has_password, verify_role
from ..utils.user_data_validation import validate_business_data
from ..utils.send_emails import send_email_pending, send_email_appeal
import json 
from ..wrap_models.business_model import BusinessInformation, Address, Moderation, BusinessRating
from django.contrib import messages

# Create your views here.

@login_required_custom
@verify_role('business')
def register_business(request):
    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
        data = json.loads(request.body)  # Parse JSON request body
        errors = validate_business_data(data)
        if errors:
            return JsonResponse({"status":"error","message":f"{errors}"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)     

    name = data.get("name")
    business_type = data.get("business_type")
    description = data.get("description")
    registration_number = data.get("registration_number")
    category = data.get("category")
    phone = data.get("phone")
    telephone = data.get("telephone")
    email = data.get("email")
    address_line_1 = data.get("address_line_1")
    address_line_2 = data.get("address_line_2")
    suburb = data.get("suburb")
    city = data.get("city")
    province = data.get("province")
    postal_code = data.get("postal_code")
    address_type = data.get("address_type")
    open_time = data.get("open_time")
    close_time = data.get("close_time")
    image = request.FILES.get('image')  # Image from the request

        # Validate image file
    if image and not image.content_type.startswith('image/'):
        return JsonResponse({'status': 'error', 'message': 'Invalid file type. Only images allowed'}, status=400)


    # Save business to the database
    business = BusinessInformation.objects.create(
        owner=request.user,
        name=name,
        business_type=business_type,
        description=description,
        registration_number=registration_number,
        category=category,
        phone=phone,
        email=email,
        open_time=open_time,
        close_time=close_time,
        image=image
    )
    
    address = Address.objects.create(
        business=business,
        address_line_1=address_line_1,
        address_line_2=address_line_2,
        suburb=suburb,
        city=city,
        province=province,
        postal_code=postal_code,
        address_type=address_type
    )

    moderator = User.objects.filter(email="sixskies25@gmail.com").first()
    moderation = Moderation.objects.create(business=business, moderator=moderator)
    send_email_pending(business)
    
    # Save the business, address, and moderation records
    business.save()
    address.save()
    moderation.save()

    # Redirect to business status page (pending status) or dashboard if approved
    if business.status == "pending":
        return redirect('business_status', business_id=business.id)
    elif business.status == "approved":
        return redirect('seller_dashboard', business_id=business.id)
    else:
        # Handle rejected or other cases
        return redirect('business_status', business_id=business.id)

@verify_role('business')
@login_required_custom
def appeal_registration(request):
    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)

    try:
        data = json.loads(request.body)  # Parse JSON request body
        errors = validate_business_data(data)
        if errors:
            return JsonResponse({"status":"error","message":f"{errors}"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)     

    business_id = data.get('business_id')
    name = data.get("name")
    business_type = data.get("business_type")
    description = data.get("description")
    registration_number = data.get("registration_number")
    category = data.get("category")
    phone = data.get("phone")
    telephone = data.get("telephone")
    email = data.get("email")
    address_line_1 = data.get("address_line_1")
    address_line_2 = data.get("address_line_2")
    suburb = data.get("suburb")
    city = data.get("city")
    province = data.get("province")
    postal_code = data.get("postal_code")
    country = data.get("country")
    address_type = data.get("address_type")
    open_time = data.get("open_time")
    close_time = data.get("close_time")

    business = BusinessInformation.objects.filter(id=int(business_id)).first()
    business.name = name
    business.business_type = business_type
    business.description = description
    business.registration_number = registration_number
    business.category = category
    business.email = email
    business.open_time = open_time
    business.close_time = close_time
    business.status = 'pending'

    address = Address.objects.filter(business=business).first()
    address.address_line_1 = address_line_1
    address.address_line_2 = address_line_2
    address.suburb = suburb
    address.city = city
    address.province = province
    address.postal_code = postal_code
    address.country = country
    address.address_type = address_type

    # Save business to the database
    moderator = User.objects.filter(email="sixskies25@gmail.com").first()
    moderation = Moderation.objects.filter(business=business, moderator=moderator).first()
    moderation.is_reviewed = False
    moderation.status = 'pending'
    send_email_appeal(business)

    # Save the updated business, address, and moderation records
    business.save()
    address.save()
    moderation.save()

    return JsonResponse({"message": "Business appeal requested successfully",'status':'success'}, status=201)


@login_required_custom
def rate_business(request):

    if not request.method == "POST":
        return JsonResponse({'status':'error', 'message':'Request method not allowed'}, status=403)
    try:
            data = json.loads(request.body)  # Parse JSON request body
    except json.JSONDecodeError:
        return JsonResponse({'message':'Invalid Json Data', "status":"error"}, status=400)     


    business = BusinessInformation.objects.filter(id=int(data.get('business_id'))).first()
    stars = int(data.get('stars'))

    is_rated = BusinessRating.objects.filter(user=request.user,business=business).first()
    if is_rated:
        return JsonResponse({'message':'You have already rated....thank you', "status":"error"}, status=400)     

    if business and stars >= 0 and stars <=5:
        rating = BusinessRating.objects.create(user=request.user,business=business,stars=stars)
        rating.save()
    else:
        return JsonResponse({'message':'Something went wrong please contact support ', "status":"error"}, status=400)     
    return JsonResponse({"message": "Thank you for rating ",'status':'success'}, status=201)



from django.views.decorators.http import require_POST

@verify_role('business')
@login_required_custom
@require_POST
def delete_business(request, business_id):
    business = get_object_or_404(BusinessInformation, id=business_id, owner=request.user)
    business.delete()
    messages.success(request, "Business deleted successfully.")
    return redirect('business')  # Use existing URL pattern

@verify_role('business')
def business_status(request, id):
    business = BusinessInformation.objects.get(id=id)
    return render(request, 'business_status.html', {'business': business})
    
