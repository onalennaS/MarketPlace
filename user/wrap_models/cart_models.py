from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from seller.wrap_models.product_model import Product, Extras,Addon
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)

    
    def total_price(self):
        product_price = self.quantity * self.product.price
        extras_price = sum(extra.price for extra in self.extras.all()) * self.quantity
        return product_price + extras_price

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class CartExtra(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="extras")
    extra = models.ForeignKey(Extras, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
   

    def __str__(self):
        return f"{self.user.username} - {self.extra.name} ({self.quantity})"

class CartAddons(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="CartAddon")
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return f"{self.cart.user.username} - {self.addon.name} ({self.quantity})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class CartDeliveryMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=50, null=True)
    added_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return f"{self.user.username} - {self.method}"

class CartDeliveryAddress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=50,null=True)
    house_no = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=50, null=True)
    complex_name = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=50, null=True)
    notes = models.CharField(max_length=200, null=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    

    instutition = models.CharField(max_length=50, null=True)
    block = models.CharField(max_length=50, null=True)
    venue = models.CharField(max_length=50, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
   

    def __str__(self):
        return f"{self.user.username} - {self.address_type} "

