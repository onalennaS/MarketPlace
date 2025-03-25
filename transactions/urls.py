from django.urls import path
from . import views



urlpatterns = [
    path('business_withdrawal/', views.business_withdrawal, name='business_withdrawal'),  # Home page URL
  ]