from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .business_model import BusinessInformation
import uuid

class Product(models.Model):
    CATEGORIES = [
        ('plate', 'Plate'),
        ('kota', 'Kota'),
        ('dagwood', 'Dagwood'),
        ('drinks', 'Drinks'),
        ('other', 'Other'),
    ]
  
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('banned', 'banned'),
        ('reected', 'rejected'),
    ]

    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    small_description = models.TextField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    is_flagged = models.BooleanField(default=False)
    sales = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to="uploads/")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    slug = models.SlugField(unique=True, blank=True)  # <--- This
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

    def is_instock(self):
        if self.quantity < 1:
            return False
        return True
    def markup_price(self):
        return float(f'{self.price}') + (float(f'{self.price}') * 0.20)
    
class ProductModeration(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_moderation")
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_moderator") 
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    status = models.CharField(max_length=20,default="pending")
    reason = models.CharField(max_length=225, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)

class RecentActivity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_activity")
    activity = models.CharField(max_length=225, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE, related_name="bp_activity")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)

class Extras(models.Model):
    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE, related_name="extras")
    name = models.CharField(max_length=225, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
   

class Addon(models.Model):
    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE, related_name="addons")
    name = models.CharField(max_length=225, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    