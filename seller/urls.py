from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    
   path('user_profile/', views.user_profile, name='user_profile'),
    
    
    path('register_business/', views.register_business, name='register_business'),
    path('register_business_form/', views.register_business_form, name='register_business_form'),
    path('business_status/', views.business_status, name='business_status'),
    
    path('business_info/', views.business_info, name='business_info'),
    path('view_stats/', views.view_stats, name='view_stats'),
    path('add_products/', views.add_products, name='add_products'),
    path('edit_products/', views.edit_products, name='edit_products'),
    path('orders/', views.orders, name='orders'),
    path('order_tracking/', views.order_tracking, name='order_tracking'),
    path('transaction/', views.transaction, name='transaction'),
    path('pay_for_premium/', views.pay_for_premium, name='pay_for_premium'),


]
