from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from seller.wrap_models.business_model import BusinessInformation
from seller.wrap_models.orders_model import Order
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"

class BusinessWallet(models.Model):
    business = models.OneToOneField(BusinessInformation, on_delete=models.CASCADE, related_name="business_wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"


class BusinessTransaction(models.Model):
    STATUS_CHOICES = [("Success", "Success"), ("Failed", "Failed"), ("Pending", "Pending")]
    ref = models.CharField(max_length=60,null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_transactions",null=True)
    receiver = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE, related_name="received_transactions",null=True)
    transaction_type = models.CharField(max_length=50,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    timestamp = models.DateTimeField(default=now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    fees = models.DecimalField(max_digits=10, decimal_places=2,null=True,default=0.00)
    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount} ({self.status})"

@receiver(pre_save, sender=BusinessTransaction)
def set_ref_id(sender, instance, **kwargs):
    if not instance.ref and instance.transaction_type == "Withdrawal":  
        last_ref = BusinessTransaction.objects.order_by("-id").first()
        next_ref = last_ref.id + 1 if last_ref else 1
        instance.ref = f"Withdrawal-{next_ref:03d}"  # e.g., ORD00001, ORD00002

# class Transaction(models.Model):
#     STATUS_CHOICES = [("Success", "Success"), ("Failed", "Failed"), ("Pending", "Pending")]
    
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_transactions")
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_transactions")
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(default=now)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

#     def __str__(self):
#         return f"{self.sender} -> {self.receiver}: {self.amount} ({self.status})"