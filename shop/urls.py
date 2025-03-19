from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_base, name='shop_base'),
    path('view_product/<int:product_id>', views.view_product, name='view_product'),

    
]