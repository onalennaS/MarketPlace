from django.urls import path
from . import views



urlpatterns = [
    path('business_withdrawal/', views.business_withdrawal, name='business_withdrawal'),  # Home page URL
    path('payment/callback/', views.payment_callback, name='payment_callback'),  # Home page URL
    path('payment/webhook/', views.paystack_webhook, name='paystack_webhook'),  # Home page URL
    
  
  ]