from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

class BusinessInformation(models.Model):
    BUSINESS_CATEGORIES = [
        ('dropship', 'Dropship'),
        ('food', 'Food & beverages'),
        ('clothing', 'Clothing'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=200)
    description = models.TextField()
    registration_number = models.CharField(max_length=200, unique=False)
    category = models.CharField(max_length=50, choices=BUSINESS_CATEGORIES, default='other')
    phone = models.CharField(max_length=20, blank=True, null=False)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=200,unique=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="businesses")
    open_time = models.CharField(max_length=50)
    close_time = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending")
    account_code = models.CharField(max_length=200,default="",null=True)
    open_orders = models.BooleanField(default=False)
    image = models.ImageField(upload_to='uploads/business_images/', null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    slug = models.SlugField( blank=True)  # <--- This
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1

            while BusinessInformation.objects.filter(slug=slug).exists():
                if BusinessInformation.objects.filter(slug=slug).first():
                    slug = f"{base_slug}-{num}"
                    num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


    def get_rating(self):
        all_ratings = BusinessRating.objects.filter(business=self)
        stars_list = [rating.stars for rating in all_ratings]

        if stars_list:
            average_rating = round(sum(stars_list) / len(stars_list), 1)
        else:
            average_rating = 0.0 
        return average_rating

    def get_item_count(self):
        products = self.products.all().count()
        return products


    class Meta:
        verbose_name_plural = "Businesses"

class Address(models.Model):
    PROVINCE_CHOICES = [
        # ('EC', 'Eastern Cape'),
        # ('FS', 'Free State'),
        ('GP', 'Gauteng'),
        # ('KZN', 'KwaZulu-Natal'),
        # ('LP', 'Limpopo'),
        # ('MP', 'Mpumalanga'),
        # ('NC', 'Northern Cape'),
        # ('NW', 'North West'),
        # ('WC', 'Western Cape'),
    ]

    ADDRESS_TYPES = [
        ('residential', 'Residential'),
        ('business', 'Business'),
        ('postal', 'Postal'),
        ('other', 'Other'),
    ]

    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE, related_name="addresses")
    address_line_1 = models.CharField(max_length=255, verbose_name="Street Address")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Complex/Apartment")
    suburb = models.CharField(max_length=100, verbose_name="Suburb")
    city = models.CharField(max_length=100, verbose_name="City/Municipality")
    province = models.CharField(max_length=100, choices=PROVINCE_CHOICES, verbose_name="Province")
    postal_code = models.CharField(max_length=50, verbose_name="Postal Code")  # SA postal codes are 4 digits
    
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='business', verbose_name="Address Type")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.address_line_1}, {self.suburb}, {self.city}, {self.province}, {self.postal_code}"

    class Meta:
        verbose_name_plural = "Addresses"

class Moderation(models.Model):
    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE, related_name="moderation")
    is_reviewed = models.BooleanField(default=False)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="moderator") 
    timestamp = models.DateTimeField(default=timezone.now, null=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    status = models.CharField(max_length=20,default="pending")
    reason = models.CharField(max_length=225, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)


class BusinessRating(models.Model):
    business = models.ForeignKey(BusinessInformation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(default=timezone.now, null=True)
    stars = models.IntegerField(null=False,default=0)

    