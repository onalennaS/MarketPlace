from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .utils import login_required_custom,is_admin
from seller.utils.authentication_utils import verify_role
# Create your views here.


@login_required_custom
@verify_role('admin')
def dashboard(request):
	return render(request, 'administrator/dashboard.html')


@login_required_custom
@verify_role('admin')
def transaction(request):
	return render(request, 'administrator/sales.html')

@login_required_custom
@verify_role('admin')
def report(request):
	return render(request, 'administrator/report.html')

@login_required_custom
@verify_role('admin')
def invoice(request):
	return render(request, 'administrator/invoice.html')


@login_required_custom
@verify_role('admin')
def settings(request):
	return render(request, 'administrator/settings.html')

