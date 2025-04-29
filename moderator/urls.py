from django.urls import path
from .views import render_views as views 
from .views import moderation_view as mod_views
from .views import product_moderation as product_views

urlpatterns = [
    path('', views.dashboard, name='moderator'),
    path('business', views.business, name='business_managment'),
    path('business/<int:business_id>', views.view_business, name='view_business'),
    path('user', views.user, name='user_management'),
    path('notificatons', views.notificatons, name='moderator_notifications'),
    path('settings', views.settings, name='moderator_settings'),
    path('product', views.product, name='moderator_product'),
    path('courier', views.courier, name='moderator_courier'),
    path('view_courier/<int:courier_id>', views.view_courier, name='view_courier'),
    
    path('courier/approve/', mod_views.approve_courier, name='moderator_approve_courier'),
    path('courier/reject/', mod_views.reject_courier, name='moderator_reject_courier'),

    path('courier/payout', views.payout, name='moderator_courier_payout'),
    path('courier/payout/approve_payout/', mod_views.approve_payout, name='moderator_courier_payout_approve_payout'),
    path('courier/payout/reject_payout/', mod_views.reject_payout, name='moderator_courier_payout_reject_payout'),


    path('view_product_moderator/<int:product_id>', views.view_product_moderator, name='moderator_view_product'), 
path('business/approve/', mod_views.approve_business, name='moderator_approve_business'),
path('business/reject/', mod_views.reject_business, name='moderator_reject_business'),
path('business/ban/', mod_views.ban_business, name='moderator_ban_business'),

path('product/approve/', product_views.approve_product, name='moderator_approve_product'),

path('product/reject/', product_views.reject_product, name='moderator_reject_product'),
   

]
