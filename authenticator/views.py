# authentication/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .validator import validate_password
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from django.shortcuts import redirect

def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect to login page if not authenticated
    return _wrapped_view



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
                messages.error(request, f'{key} if a required field')
                return render(request, 'authentication/signup.html', {'data':data})

        email_exists = User.objects.filter(username=data['email'])
        if email_exists:
            messages.error(request,f'email {data['email']} is already taken')
            return render(request, 'authentication/signup.html', {'data':data})
        
        username_exists = User.objects.filter(username=data['username'])
        if username_exists:
            messages.error(request,f'username {data['username']} is already taken')
            return render(request, 'authentication/signup.html', {'data':data})

        is_password_valid = validate_password(data['password'], data['confirm_password'])
        if  is_password_valid != True:
            messages.error(request,f'{is_password_valid}')
            return render(request, 'authentication/signup.html', {'data':data})

        user = User.objects.create(username=data['username'],email=data['email'], password=make_password(data['password']))
        user.save()
        
        messages.success(request,f'Account created successfully proceed')
        return redirect('signin')

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

        user = User.objects.filter(username=data['username']).first()
        if user:
            if check_password(data['password'],user.password):
                login(request, user)
                messages.success(request,f'logged in successfully as {user.username}')
                return redirect('user_profile')        
            else:
                messages.error(request,'Password is incorrect')
                return render(request, 'authentication/signin.html', {'data':data})
        else:
            messages.error(request,f"Username '{data['username']}' does not exists..")
            return render(request, 'authentication/signin.html', {'data':data})

    return render(request, 'authentication/signin.html')

@login_required_custom
def home(request):
    if request.user.is_authenticated:
        return HttpResponse(f'Logged in successfully {request.user}')
    else:
        messages.error(request,'you are not logged in ')
        return redirect('login')

def logout_view(request):
    messages.error(request,"Logged out successfully")
    logout(request)
    return redirect('signin')  
