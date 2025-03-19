from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('report/', views.report, name='admin_report'),

    path('transaction/', views.transaction, name='admin_transaction'),
   
    path('settings/', views.settings, name='admin_settings'),
    path('invoice/', views.invoice, name='invoice'),

   


   

]