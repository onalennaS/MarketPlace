from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('verify_user/', views.verify_user, name='verify_user'),
   
    path('create_password/', views.create_password, name='create_password'),
    path('request_password_reset/', views.request_password_reset, name='password_reset'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('reset-password/<token>/', views.reset_password, name='reset_password'),
    path('verify_email/<token>/', views.verify_email, name='verify_email'),
    path('activate_account/<email>', views.activate_account, name='activate_account'),

    
    
]
