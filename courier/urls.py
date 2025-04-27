from django.urls import path
from .views import courier_views,render_views as views 


urlpatterns = [
    path('', views.courier_home, name='courier_home'),
    path('courier_orders/', views.courier_orders, name='courier_orders'),
    path('courier_earnings/', views.courier_earnings, name='courier_earnings'),
    path('courier_delivery/', views.courier_delivery, name='courier_delivery'),
    path('courier_home/', views.courier_home, name='courier_home'),
    path('courier_register/', views.courier_register, name='courier_register'),
    path('courier_status/', views.courier_status, name='courier_status'),
    path('courier/rejected/', views.courier_rejected, name='courier_rejected'),
    path('courier/move_delivery_next_stage/', courier_views.move_delivery_next_stage, name='move_delivery_next_stage'),
  	

  
]