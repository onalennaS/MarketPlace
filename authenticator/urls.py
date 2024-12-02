from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('create_password/', views.create_password, name='create_password'),
    path('request_password_reset/', views.request_password_reset, name='password_reset'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('reset-password/<token>/', views.reset_password, name='reset_password'),

    
]
