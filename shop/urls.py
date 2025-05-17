from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.shop_base, name='shop_base'),
    path('<slug:bSlug>/<slug:pSlug>', views.view_product, name='view_product'),
    path('<slug:slug>', views.view_business_products, name='view_business_products'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]