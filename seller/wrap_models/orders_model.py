from django.db import models
from django.contrib.auth.models import User
from .product_model import Product, Extras, Addon
from seller.wrap_models.business_model import BusinessInformation
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
 
class Order(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    order_id = models.CharField(max_length=20, unique=True, blank=True)  # Custom Order ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Order Total
    delivery_method = models.CharField(max_length=50,null=True)
    ref = models.CharField(max_length=250,null=True,default="")
    paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Processing", "Processing"),("On route", "On route"), ("Delivered", "Delivered"), ("Failed", "Failed")],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
 
    def total_price(self):
        amount = 0
        for item in self.order_items.all():
            product_price = item.quantity * item.product.price
            extras_price = sum(extra.extra.price for extra in self.extras.all()) * item.quantity
            amount += product_price + extras_price
        if self.delivery_method == "delivery":
            amount += 15
        return amount

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

# ✅ Use a `pre_save` signal to generate `order_id`
@receiver(pre_save, sender=Order)
def set_order_id(sender, instance, **kwargs):
    if not instance.order_id:  
        last_order = Order.objects.order_by("-id").first()
        next_id = last_order.id + 1 if last_order else 1
        instance.order_id = f"ORD{next_id:05d}"  # e.g., ORD00001, ORD00002


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
   

    def total_price(self):
        product_price = self.quantity * self.product.price
        extras_price = sum(extra.price for extra in self.extras.all()) * self.quantity
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
