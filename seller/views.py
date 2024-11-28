from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
def base(request):
    return render(request, 'seller/base.html')