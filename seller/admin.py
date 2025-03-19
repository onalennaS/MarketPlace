from django.contrib import admin

from .wrap_models.business_model import BusinessInformation, Address, Moderation
# Register your models here.


# Simple model registration
admin.site.register(BusinessInformation)
admin.site.register(Address)
admin.site.register(Moderation)
