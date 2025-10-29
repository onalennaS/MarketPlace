from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from seller.wrap_models.orders_model import Order

class Courier(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courier")
	phone_number = 	models.CharField(max_length=225, null=True)
	vehicle_type = models.CharField(max_length=225, null=False)	
	profile_image = models.CharField(max_length=225, null=True)
	total_deliveries = models.IntegerField(default=0)
	total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	status = models.CharField(max_length=200,default="pending ")
	is_reviewed = models.BooleanField(default=False)
	created_at = models.DateTimeField(default=timezone.now)

class OrderDelivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="delivery", null=True)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    address = models.CharField(max_length=200,null=False)
    note = models.CharField(max_length=200,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_taken = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="available")
    created_at = models.DateTimeField(default=timezone.now)


