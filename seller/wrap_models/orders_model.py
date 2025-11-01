from django.db import models
from django.contrib.auth.models import User
from .product_model import Product, Extras, Addon
from seller.wrap_models.business_model import BusinessInformation
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import uuid
import random
from user.models import ReferralProfile, Referral

class Order(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    order_id = models.CharField(max_length=20, unique=True, blank=True)  # Custom Order ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Order Total
    delivery_method = models.CharField(max_length=50,null=True)
    ref = models.CharField(max_length=250,null=True,default="")
    paid = models.BooleanField(default=False)
    drop_codes = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Processing", "Processing"),("On route", "On route"), ("Delivered", "Delivered"), ("Failed", "Failed")],
        default="Pending"
    )
    created_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
 
    def total_price(self):
        amount = 0
        for item in self.order_items.all():
            product_price = item.quantity * item.product.price
            extras_price = sum(extra.extra.price for extra in self.extras.all()) * item.quantity
            amount += product_price + extras_price
        if self.delivery_method == "delivery":
            amount += 10
        return amount

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

#######
@receiver(post_save, sender=Order)
def create_user_profile(sender, instance, created, **kwargs):
    """
    This function runs every time a User is saved.
    """
    if created:  # Only run when a new User is created
        orders = Order.objects.filter(user=instance.user).all()
        if len(orders) < 2 :
            referrered = ReferralProfile.objects.filter(user=instance.user).first()
            
            referrer = ReferralProfile.objects.filter(user=referrered.referred_by).first()
            referrer.wallet_balance += 5
            referrer.total_earned += 5
            referrer.purchases += 1 
            referrer.save()
            ref_reward = Referral.objects.create(referrer=referrer.user,referred=instance.user,is_rewarded=True,reward=5,referral_type="purchase")
            ref_reward.save()

# ✅ Use a `pre_save` signal to generate `order_id`
@receiver(pre_save, sender=Order)
def set_order_id(sender, instance, **kwargs):
    if not instance.order_id:
        last_order = Order.objects.order_by("-id").first()
        next_id = last_order.id + 1 if last_order else 1
        instance.order_id = f"ORD{next_id:05d}"  # e.g., ORD00001, ORD00002

# ✅ Use a `pre_save` signal to generate `drop_code`
@receiver(pre_save, sender=Order)
def set_drop_code(sender, instance, **kwargs):
    if not instance.drop_codes:
        while True:
            # Generate a random 5-digit code
            code = f"{random.randint(10000, 99999)}"
            # Check if this code is already in use
            if not Order.objects.filter(drop_codes=code).exists():
                instance.drop_codes = code
                break

# ✅ Use a `pre_save` signal to set `estimated_delivery`
@receiver(pre_save, sender=Order)
def set_estimated_delivery(sender, instance, **kwargs):
    if not instance.estimated_delivery:
        instance.estimated_delivery = timezone.now() + timedelta(minutes=37)

@receiver(pre_save, sender=Order)
def set_created_at(sender, instance, **kwargs):
    if not instance.created_at:
        instance.created_at = timezone.now()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(null=True, blank=True)

@receiver(pre_save, sender=OrderItem)
def set_created_at(sender, instance, **kwargs):
    if not instance.created_at:
        instance.created_at = timezone.now()

    def total_price(self):
        product_price = self.quantity * self.product.price
        extras_price = sum(extra.extra.price for extra in self.order.extras.all()) * self.quantity
        return product_price + extras_price

    def __str__(self):
        return f"{self.order.user.username} - {self.product.name} ({self.quantity})"

class OrderExtra(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="extras")
    extra = models.ForeignKey(Extras, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
   

    def __str__(self):
        return f"{self.order.user.username} - {self.extra.name} ({self.quantity})"

class OrderAddons(models.Model):
    product = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="CartAddon")
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.order.user.username} - {self.addon.name} ({self.quantity})"

class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_address")
    address_line_1 = models.CharField(max_length=100,null=True)
    address_line_2 = models.CharField(max_length=100,null=True)
    address_line_3 = models.CharField(max_length=100,null=True)
    address_line_4 = models.CharField(max_length=100,null=True)
    notes = models.CharField(max_length=200,null=True)
    
    

    def __str__(self):
        return f"{self.order.user.username} - {self.addon.name} ({self.quantity})"
