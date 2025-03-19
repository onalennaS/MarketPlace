from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from seller.wrap_models.product_model import Product, Extras,Addon


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        product_price = self.quantity * self.product.price
        extras_price = sum(extra.price for extra in self.extras.all()) * self.quantity
        return product_price + extras_price

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class CartExtra(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="extras")
    extra = models.ForeignKey(Extras, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username} - {self.extra.name} ({self.quantity})"

class CartAddons(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="CartAddon")
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username} - {self.addon.name} ({self.quantity})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"