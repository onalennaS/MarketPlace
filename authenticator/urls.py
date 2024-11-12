from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
]
