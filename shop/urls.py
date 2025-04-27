from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.shop_base, name='shop_base'),
    path('view_product/<int:product_id>', views.view_product, name='view_product'),
    path('view_business_products/<int:business_id>', views.view_business_products, name='view_business_products'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('app.py/', views.app_py, name='app.py'),
    path('templates/home.html', views.home_html),
    path('templates/login.html', views.login_html),
]