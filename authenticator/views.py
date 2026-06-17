# authentication/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .validator import validate_password, validate_south_african_phone
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from django.shortcuts import redirect
from .utils import send_email_reset_link, login_required_custom,generate_reset_token, verify_reset_token,send_verify_email, verify_role
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from courier.models import Courier
from user.models import  ReferralProfile,Referral

User = get_user_model()

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        # Local/dev behavior: auto-activate accounts so they don't require email verification
        # (keeps functionality working even when local email sending is not configured)

        data = {
        'username' : request.POST.get('username').strip(),
        'email' : request.POST.get('email').strip(),
        'role' : request.POST.get('role').strip(),
        'password' : request.POST.get('password').strip(),
        'confirm_password' : request.POST.get('confirm_password').strip()
        }
        for key, value in data.items():
            if not value:
                messages.error(request, f'{key} is a required field')
                return render(request, 'authentication/signup.html', {'data':data})

        email_exists = User.objects.filter(username=data['email']).first()
        if email_exists:
            messages.error(request,f"email {data['email']} is already taken")
            return render(request, 'authentication/signup.html', {'data':data})
        username_exists = User.objects.filter(username=data['username']).first()
        if username_exists:
            messages.error(request,f"username {data['username']} is already taken")
            return render(request, 'authentication/signup.html', {'data':data})

        is_password_valid = validate_password(data['password'], data['confirm_password'])
        if  is_password_valid != True:
            messages.error(request,f'{is_password_valid}')
            return render(request, 'authentication/signup.html', {'data':data})

        user = User.objects.create(username=data['username'],email=data['email'], password=make_password(data['password']), is_active=True)
        user.save()


        # Assign role based on selection
        if data['role'] == 'buyer':
            group = Group.objects.filter(name="customer").first()
            if group:
                user.groups.add(group)
        elif data['role'] == 'seller':
            group = Group.objects.filter(name="business").first()
            if group:
                user.groups.add(group)
        elif data['role'] == 'driver':
            group = Group.objects.filter(name="courier").first()
            if group:
                user.groups.add(group)
                # Create Courier profile for driver
                courier = Courier.objects.create(user=user, phone_number='', vehicle_type='')  # Phone and vehicle can be updated later
                courier.save()

        if 'code' in request.session:
            referrer = ReferralProfile.objects.filter(referral_code=request.session['code']).first()
            new_profile = ReferralProfile.objects.create(user=user,is_referred=True,referred_by=referrer.user)
            referrer.wallet_balance += 2
            referrer.total_earned += 2
            referrer.signups += 1
            new_profile.save()
            ref_reward = Referral.objects.create(referrer=referrer.user,referred=user,is_rewarded=True,reward=2,referral_type="signup")
            ref_reward.save()
        messages.success(request,f'Account created successfully proceed')
        sent = send_verify_email(user.email)
        if not sent:
            messages.error(request, 'Account created but verification email could not be sent. Check server logs / Gmail OAuth credentials.')
        # No activation step required for buyers (account is created as active)
        return redirect('signin')

    return render(request, 'authentication/signup.html')



def register_delivery(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        data = {
        'username' : request.POST.get('username').strip(),
        'email' : request.POST.get('email').strip(),
        'phone_number' : request.POST.get('phone_number').strip(),
        'vehicle_type' : request.POST.get('vehicle_type').strip(),
        'password' : request.POST.get('password').strip(),
        'confirm_password' : request.POST.get('confirm_password').strip()
        }
        for key, value in data.items():
            if not value:
                messages.error(request, f'{key} is a required field')
                return render(request, 'authentication/signup_courier.html', {'data':data})

        email_exists = User.objects.filter(username=data['email']).first()
        if email_exists:
            messages.error(request,f"email {data['email']} is already taken , /n note: if this mail belongs to you please log in then click become driver button on menu")
            return render(request, 'authentication/signup_courier.html', {'data':data})

        email_exists = User.objects.filter(email=data['email']).first()
        if email_exists:
            messages.error(request,f"email {data['email']} is already taken , /n note: if this mail belongs to you please log in then click become driver button on menu")
            return render(request, 'authentication/signup_courier.html', {'data':data})
        
        username_exists = User.objects.filter(username=data['username'])
        if username_exists:
            messages.error(request,f"username {data['username']} is already taken , /n note: if this mail belongs to you please log in then click become driver button on menu")
            return render(request, 'authentication/signup_courier.html', {'data':data})

        is_password_valid = validate_password(data['password'], data['confirm_password'])
        if  is_password_valid != True:
            messages.error(request,f'{is_password_valid}')
            return render(request, 'authentication/signup_courier.html', {'data':data})

        is_phone_number_valid = validate_south_african_phone(data['phone_number'])
        if  is_phone_number_valid != True:
            messages.error(request,f'{is_phone_number_valid}')
            return render(request, 'authentication/signup_courier.html', {'data':data})

        user = User.objects.create(username=data['username'],email=data['email'], password=make_password(data['password']), is_active=True)
        user.save()

        courier = Courier.objects.create(user=user,phone_number=data['phone_number'],vehicle_type=data['vehicle_type'])
        courier.save()
        group = Group.objects.filter(name="courier").first()
        if group and user:
            user.groups.add(group)
            user.save()
        messages.success(request,f'Account created successfully proceed')
        sent = send_verify_email(user.email)
        if not sent:
            messages.error(request, 'Account created but verification email could not be sent. Check server logs / Gmail OAuth credentials.')
        return redirect('signin')


    return render(request, 'authentication/signup_courier.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'role': request.POST.get('role')
        }
        for key, value in data.items():
            if not value and key != 'role':  # role is optional
                messages.error(request,f'{key} is a required field')
                return render(request, 'authentication/signin.html', {'data':data})
        user = User.objects.filter(email=data['username']).first()
        if not user:
            user = User.objects.filter(username=data['username']).first()
        if user:
            if check_password(data['password'],user.password):

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                messages.success(request,f'logged in successfully as {user.username}')
                return redirect(verify_role(user))
            else:
                messages.error(request,'Password is incorrect')
                return render(request, 'authentication/signin.html', {'data':data})
        else:
            messages.error(request,f"Username '{data['username']}' does not exists..")
            return render(request, 'authentication/signin.html', {'data':data})
    
    # Check if redirected from seller page access attempt
    seller_access = request.GET.get('seller_access', '0')
    context = {}
    if seller_access == '1':
        messages.error(request, 'You need to sign in as a seller to access the seller page.')
        context['show_seller_message'] = True
    
    return render(request, 'authentication/signin.html', context)


def create_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST": 
        data = {
        'password' : request.POST.get('password').strip(),
        'confirm_password' : request.POST.get('confirm_password').strip()
        }
        is_password_valid = validate_password(data['password'], data['confirm_password'])
        if  is_password_valid != True:
            messages.error(request,f'{is_password_valid}')
            return render(request, 'authentication/create_password.html', {'data':data})
        request.user.password = make_password(data['password'])
        request.user.save()
        send_verify_gmail(request.user.email)
        if 'code' in request.session:
            referrer = ReferralProfile.objects.filter(referral_code=request.session['code']).first()
            new_profile = ReferralProfile.objects.create(user=request.user,is_referred=True,referred_by=referrer.user)
            new_profile.save()
            ref_reward = Referral.objects.create(referrer=referrer.user,referred=request.user,is_rewarded=True,reward=5,referral_type="signup")
            ref_reward.save()
        return redirect(verify_role(request.user))
    return render(request,'authentication/create_password.html')

def logout_view(request):
    messages.error(request,"Logged out successfully")
    logout(request)
    return redirect('signin')  
    

def verify_email(request, token):
    email = verify_reset_token(token)
    if not email:
        return render(request, 'authentication/acivation_invalid.html')
    user = User.objects.filter(email=email).first()
    if not user:
        return render(request, 'authentication/activation_invalid.html')   
    user.is_active = True
    user.save()
    messages.success(request,f'Email Verified successfully. Your account has been activated!')
    return redirect('signin')


def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        reset_token = generate_reset_token(email)
        reset_link = f"{settings.SITE_URL}/auth/reset-password/{reset_token}/"
        send_email_reset_link(email, reset_link)
        return redirect('password_reset_done')
    return render(request, 'authentication/password_reset_request.html')


def reset_password(request, token):
    email = verify_reset_token(token)
    if not email:
        return render(request, 'authentication/reset_password_invalid.html')
    user = User.objects.filter(email=email).first()
    if not user:
        return render(request, 'authentication/reset_password_invalid.html')

    if request.method == "POST": 
        data = {
        'password' : request.POST.get('password').strip(),
        'confirm_password' : request.POST.get('confirm_password').strip()
        }
        is_password_valid = validate_password(data['password'], data['confirm_password'])
        if  is_password_valid != True:
            messages.error(request,f'{is_password_valid}')
            return render(request, 'authentication/reset_password.html', {'email': email})
        user.password = make_password(data['password'])
        user.is_verified = True
        user.is_active = True
        user.save()
        return render(request, 'authentication/password_reset_success.html')
    return render(request, 'authentication/reset_password.html', {'email': email})

def password_reset_done(request):
    return render(request, 'authentication/password_reset_done.html')

def activate_account(request, email):
    if request.method == "POST":
        sent = send_verify_email(email)
        if sent:
            messages.success(request,f'Verification email sent')
        else:
            messages.error(request,'Could not send verification email. Check server logs / Gmail OAuth credentials.')
    return render(request, 'authentication/activate_account.html',{'email':email})

def verify_user(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    role = verify_role(request.user)
    print(role)
    return redirect(role)
    return redirect(verify_role(request.user))

def not_allowed(request):
    return render(request,'authentication/errors/not_allowed.html')