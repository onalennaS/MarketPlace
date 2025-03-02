from django.shortcuts import render
from .utils import login_required_custom



@login_required_custom
def dashboard(request):
	return render(request, 'moderator/dashboard.html')