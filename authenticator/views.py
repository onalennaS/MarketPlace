# authentication/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .validator import validate_password
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from django.shortcuts import redirect
from .utils import send_email_reset_link, login_required_custom,generate_reset_token, verify_reset_token,send_verify_email, verify_role
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        data = {
        'username' : request.POST.get('username').strip(),
        'email' : request.POST.get('email').strip(),
        'password' : request.POST.get('password').strip(),
        'confirm_password' : request.POST.get('confirm_password').strip()
        }
        for key, value in data.items():
            if not value:
                messages.error(request, f'{key} is a required field')
                return render(request, 'authentication/signup.html', {'data':data})

        email_exists = User.objects.filter(username=data['email'])
        if email_exists:
            messages.error(request,f"email {data['email']} is already taken")
            return render(request, 'authentication/signup.html', {'data':data})
        username_exists = User.objects.filter(username=data['username'])
        if username_exists:
            messages.error(request,f"username {data['username']} is already taken")
            return render(request, 'authentication/signup.html', {'data':data})

        is_password_valid = validate_password(data['password'], data['confirm_password'])
        if  is_password_valid != True:
            messages.error(request,f'{is_password_valid}')
            return render(request, 'authentication/signup.html', {'data':data})

        user = User.objects.create(username=data['username'],email=data['email'], password=make_password(data['password']), is_active=False)
        user.save()
        
        messages.success(request,f'Account created successfully proceed')
        send_verify_email(user.email)
        return redirect('activate_account', email=user.email)

    return render(request, 'authentication/signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password')
        }
        for key, value in data.items():
            if not value:     
                messages.error(request,f'{key} if a required field')
                return render(request, 'authentication/signin.html', {'data':data})
        user = User.objects.filter(email=data['username']).first()
        if not user:
            user = User.objects.filter(username=data['username']).first()
        if user:
            if user.is_active == False :
                return redirect('activate_account',email=user.email)
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
    return render(request, 'authentication/signin.html')


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
        return redirect('buyer_dashboard')
    return render(request, 'authentication/create_password.html')

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
        send_verify_email(email)
        messages.success(request,f'email submitted')
    return render(request, 'authentication/activate_account.html',{'email':email})

def verify_user(request):
    if not request.user.is_authenticated:
        return redirec('signin')
    return redirect(verify_role(request.user))