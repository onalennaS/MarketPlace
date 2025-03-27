from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from functools import wraps
from ..utils.authentication_utils import login_required_custom, has_password
from ..utils.user_data_validation import validate_business_data
from ..utils.send_emails import send_email_pending, send_email_appeal
import json 
from ..wrap_models.business_model import BusinessInformation, Address, Moderation

# Create your views here.
# Create your views here.

@login_required_custom
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
                close_time=close_time
                
            )
    address = Address.objects.create(
                business=business,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                suburb=suburb,
                city=city,
                province=province,
                postal_code=postal_code,
                
                address_type=address_type)

    moderator = User.objects.filter(email="sixskies25@gmail.com").first()
    moderation = Moderation.objects.create(business=business,moderator=moderator)
    send_email_pending(business)
    business.save()
    address.save()
    moderation.save()
    return JsonResponse({"message": "Business created successfully",'status':'success','id':business.id}, status=201)

    
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
    moderation = Moderation.objects.filter(business=business,moderator=moderator).first()
    moderation.is_reviewed = False
    moderation.status = 'pending'
    send_email_appeal(business)
    business.save()
    address.save()
    moderation.save()
    return JsonResponse({"message": "Business appeal requested successfully",'status':'success'}, status=201)

    
