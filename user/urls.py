from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('dashboard/buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/order_history/', views.order_history, name='order_history'),
    path('dashboard/order_history/view-order-details/', views.view_order_details, name='order_details'),
    path('dashboard/wish_lists/', views.wish_lists, name='wish_lists'),
    path('dashboard/track_orders/', views.track_orders, name='track_orders'),
    path('dashboard/buyer_reviews/', views.buyer_reviews, name='buyer_reviews'),
    path('dashboard/referrals_earnings', views.referrals_earnings, name='referrals_earnings'),
    path('dashboard/gift_card', views.gift_card, name='gift_card'),
    path('dashboard/credit', views.credit, name='credit'),
    path('dashboard/cart', views.cart, name='cart'),
    path('dashboard/account_settings/', views.account_settings, name='account_settings'),
    path('dashboard/buyer_support/', views.buyer_support, name='buyer_support'),
    path('dashboard/address', views.address, name='address'),
    path('dashboard/', views.dash, name='dash'),

    
   
   
]
