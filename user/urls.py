from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('order_history/', views.order_history, name='order_history'),
    path('wish_lists/', views.wish_lists, name='wish_lists'),
    path('track_orders/', views.track_orders, name='track_orders'),
    path('buyer_reviews/', views.buyer_reviews, name='buyer_reviews'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('buyer_support/', views.buyer_support, name='buyer_support'),
   
]
