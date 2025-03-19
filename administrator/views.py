from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .utils import login_required_custom,is_admin
# Create your views here.

@login_required_custom
@user_passes_test(is_admin, login_url="/no-access/")
def dashboard(request):
	return render(request, 'administrator/dashboard.html')


@login_required_custom
def transaction(request):
	return render(request, 'administrator/sales.html')

@login_required_custom
def report(request):
	return render(request, 'administrator/report.html')

@login_required_custom
def invoice(request):
	return render(request, 'administrator/invoice.html')


@login_required_custom
def settings(request):
	return render(request, 'administrator/settings.html')

