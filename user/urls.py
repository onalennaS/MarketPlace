from django.urls import path
from . import views
from .wrap_views import cart_views


urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('dashboard/buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/order_history/', views.order_history, name='order_history'),
    path('dashboard/order_history/view-order-details/<int:order_id>', views.view_order_details, name='order_details'),
    path('dashboard/wish_lists/', views.wish_lists, name='wish_lists'),
    path('dashboard/track_orders/<int:order_id>/', views.track_orders, name='track_orders'),
    path('dashboard/buyer_reviews/', views.buyer_reviews, name='buyer_reviews'),
    path('dashboard/referrals_earnings', views.referrals_earnings, name='referrals_earnings'),
    path('dashboard/gift_card', views.gift_card, name='gift_card'),
    path('dashboard/credit', views.credit, name='credit'),
    path('dashboard/cart', views.cart, name='cart'),
    path('dashboard/checkout', views.checkout, name='checkout'),
    path('dashboard/account_settings/', views.account_settings, name='account_settings'),
    path('dashboard/buyer_support/', views.buyer_support, name='buyer_support'),
    path('dashboard/address', views.address, name='address'),
    path('dashboard/payment_history', views.payment_history, name='payment_history'),
    path('dashboard/checkout/payment_successful/<int:order_id>', views.payment_successful, name='payment_successful'),
    path('dashboard/subscription_plan', views.subscription_plan, name='subscription_plan'),
    path('dashboard/', views.dash, name='dash'),

    

    path('api/user/add_cart/', cart_views.add_cart, name='add_cart'),
    path('api/user/add_extra_to_cart/', cart_views.add_extra_to_cart, name='add_extra_to_cart'),
    path('api/user/delete_extra/', cart_views.delete_extra, name='delete_extra'),
    
    path('api/user/delete_cart/', cart_views.delete_cart, name='delete_cart'),

    path('api/user/add_wishlist/', cart_views.add_wishlist, name='add_wishlist'),
    path('api/user/add_cart_delivery_method/', cart_views.add_cart_delivery_method, name='add_cart_delivery_method'),
    path('api/user/add_cart_delivery_address/', cart_views.add_cart_delivery_address, name='add_cart_delivery_address'),
    path('api/user/checkout/palce_order/', cart_views.palce_order, name='palce_order'),
    
  
]
