from django.contrib import admin

from .wrap_models.business_model import BusinessInformation, Address, Moderation
# Register your models here.
from .wrap_models.orders_model import  Order, OrderItem, OrderExtra, OrderAddons, OrderAddress
from .wrap_models.product_model import Product, ProductModeration, RecentActivity, Extras, Addon
# Simple model registration
admin.site.register(BusinessInformation)
admin.site.register(Address)
admin.site.register(Moderation)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderExtra)
admin.site.register(OrderAddons)
admin.site.register(OrderAddress)
admin.site.register(Product)
admin.site.register(ProductModeration)
admin.site.register(RecentActivity)
admin.site.register(Extras)
admin.site.register(Addon)
