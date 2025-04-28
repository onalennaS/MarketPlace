from django.shortcuts import render, redirect
# from .utils import login_required_custom, has_password
from allauth.socialaccount.models import SocialAccount
from user.wrap_models.cart_models import Cart , Wishlist,CartDeliveryMethod, CartDeliveryAddress, CartExtra
from seller.wrap_models.orders_model import Order, OrderItem, OrderExtra, OrderAddress
from decimal import Decimal
from seller.utils.authentication_utils import login_required_custom, verify_role
from ..utils import validate_full_name, validate_dob,validate_phone,validate_email, validate_address, validate_file_uploaded, validate_sa_id, validate_file_uploaded, validate_transport, validate_agreements
from ..models import Courier, OrderDelivery
from django.contrib.auth.models import Group
from django.utils import timezone
from transactions.models import DeliveryWallet, DeliveryTransaction


@login_required_custom 
def courier_home(request):
    return render(request, 'courier/driver_landing_page.html')


@login_required_custom 
def courier_register(request):
    courier_exists = Courier.objects.filter(user=request.user).first()
    if courier_exists:
        if courier_exists.is_reviewed:
            if courier_exists.status == "approved":
                return redirect('courier_orders')
            else:
                return redirect('courier_rejected')
        else:
            return redirect('courier_status')
    if request.method == "POST":
        full_name = request.POST['full_name']
        dob = request.POST['dob']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        profile_picture = request.FILES.get('profile_picture')
        id_number = request.POST['id_number']
        id_upload = request.FILES.get('id_upload')
        transport = request.POST['transport']
        terms_and_conditions_check = request.POST['terms_and_conditions_check'] == 'on'
        privacy_policy_check = request.POST['privacy_policy_check'] == 'on'
        code_of_conduct_check = request.POST['code_of_conduct_check'] == 'on'
        print(profile_picture)
        print(id_upload)
        # validators 
        errors = []

        # if not validate_full_name(full_name):
        #     errors.append("Please enter a valid full name.")
        # if not validate_dob(dob):
        #     errors.append("Invalid date of birth. You must be 16 years or older.")
        # if not validate_phone(phone):
        #     errors.append("Invalid South African phone number.")
        # if not validate_email(email):
        #     errors.append("Invalid email address.")
        # if not validate_address(address):
        #     errors.append("Please provide your address.")
        # if not validate_file_uploaded(profile_picture):
        #     errors.append("Please upload a profile picture.")
        # if not validate_sa_id(id_number):
        #     errors.append("Invalid South African ID number.")
        # if not validate_file_uploaded(id_upload):
        #     errors.append("Please upload a copy of your ID.")
        # if not validate_transport(transport):
        #     errors.append("Please select a valid transport option.")
        # if not validate_agreements(terms_and_conditions_check, privacy_policy_check, code_of_conduct_check):
        #     errors.append("You must agree to all policies to continue.")

        if errors:
            return render(request, 'courier/register_courier.html',{'errors':errors})


        courier_exists = Courier.objects.filter(user=request.user,vehicle_type="transport").first()
        if courier_exists:
            return render(request, 'courier/register_courier.html',{'errors':"courier account already exists"})

        courier = Courier(user=request.user,vehicle_type="transport")
        courier.save()
        group = Group.objects.filter(name="courier").first()
        if group and request.user:
            request.user.groups.add(group)
            request.user.save()
        return render(request,'courier/register_courier.html',{'message':'success'})
    return render(request, 'courier/register_courier.html')

@login_required_custom 
@verify_role('courier')
def courier_dash(request):
    return render(request, 'courier/base.html')

@login_required_custom
@verify_role('courier')
def courier_orders(request):
    all_orders = OrderDelivery.objects.all()
    available_order = all_orders.filter(is_taken=False).all()
    waiting_orders = all_orders.filter(user=request.user,status="waiting").all()
    inprogress_orders = all_orders.filter(user=request.user,status="inprogress").all()
    delivered_orders = all_orders.filter(user=request.user,status="delivered").all()
    return render(request, 'courier/orders.html',{'available_orders':available_order,'waiting_orders':waiting_orders,'inprogress_orders':inprogress_orders,'delivered_orders':delivered_orders})

@login_required_custom
@verify_role('courier')
def courier_earnings(request):
    wallet = DeliveryWallet.objects.filter(user=request.user).first()
    total = 0.00
    balance = 0.00
    if wallet :
        total = wallet.total
        balance = wallet.balance
    all_trans = DeliveryTransaction.objects.filter(user=request.user).all()
    pending_trans = all_trans.filter(status="Pending").all()
    amount_pending = 0.00
    for pending_tran in pending_trans:
        amount_pending += float(pending_tran.amount)
    return render(request, 'courier/earnings.html',{'total':total,'balance':balance,'pending':amount_pending,"delivery_transactions":all_trans})

@login_required_custom
@verify_role('courier')
def courier_delivery(request):
    today = timezone.now().date()  # Get today's date (only the date part, no time)
    all_deliveries = OrderDelivery.objects.filter(user=request.user).all()
    total_count = all_deliveries.count()
    pending_count = all_deliveries.filter(status="inprogress").all().count()
    today_counts = all_deliveries.filter(created_at__date=today).all().count()
    return render(request, 'courier/delivery.html',{'total_count':total_count,'pending_count':pending_count,"today_counts":today_counts,'all_deliveries':all_deliveries})



@login_required_custom
@verify_role('courier')
def courier_status(request):
    return render(request, 'courier/status.html')

@login_required_custom
@verify_role('courier')
def courier_rejected(request):
    return render(request, 'courier/rejected.html')