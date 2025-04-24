from django.urls import path

from .views.render_views import (user_profile,
                                  base,
                                  dashboard,
                                  business,
                                  register_business_form,
                                  business_status,
                                  business_info,
                                  view_stats,
                                  add_products,
                                  edit_products,
                                  orders,
                                  order_tracking,
                                  transaction,
                                  pay_for_premium,
                                  manage_product,
                                  reviews,
                                  settings,
                                  customer,
                                  invoice,
                                  report,
                                  appeal_registration_view,
                                  view_product
                                  )

from .views.business_views import register_business, appeal_registration, delete_business
from .views.product_views import add_product as api_add_product, delete_product, edit_product as ep, add_extras, delete_extras, add_addons, delete_addon
from .views.order_views import move_order_next_stage, stop_order, start_order


urlpatterns = [
    path('', base, name='base'),
    path('user_profile/', user_profile, name='user_profile'),
    path('dashboard/<int:business_id>', dashboard, name='seller_dashboard'),
    path('business/', business, name='business'),
    path('register_business_form/', register_business_form, name='register_business_form'),
    path('business_status/<int:business_id>', business_status, name='business_status'),
    path('appeal_registration_view/<int:business_id>', appeal_registration_view, name='appeal_registration_view'),
    path('business_info/', business_info, name='business_info'),
    path('view_stats/', view_stats, name='view_stats'),
    
    path('edit_products/<int:business_id>/<int:product_id>', edit_products, name='edit_products'),
    path('view_product/<int:product_id>', view_product, name='view_product_admin'),
    
    path('orders/<int:business_id>', orders, name='orders'),
    path('order_tracking/', order_tracking, name='order_tracking'),
    path('transaction/<int:business_id>', transaction, name='transaction'),
    path('pay_for_premium/', pay_for_premium, name='pay_for_premium'),
    path('manage_product/<int:business_id>', manage_product, name='manage_product'),
    path('reviews/', reviews, name='reviews'),
    path('settings/', settings, name='settings'),
    path('customer/<int:business_id>', customer, name='customer'),
    path('invoice/', invoice, name='invoice'),
    path('report/', report, name='report'),
    path('add_products/<int:business_id>', add_products, name='add_products'),
    
    path('api/add_extra/', add_extras, name='api_add_extras'),
    path('api/delete_extra/', delete_extras, name='api_delete_extras'),
    path('api/delete_product/', delete_product, name='api_delete_product'),
    path('api/edit_product/', ep, name='api_edit_product'),
    path('api/add_product/', api_add_product, name='api_add_product'),
    path('api/appeal_registration/', appeal_registration, name='appeal_registration'),
    path('api/register_business/', register_business, name='register_business'),
    path('api/add_addons/', add_addons, name='add_addons'),
    path('api/delete_addon/', delete_addon, name='delete_addon'),
    path('api/stop_order/', stop_order, name='stop_order'),
    path('api/start_order/', start_order, name='start_order'),
    path('api/move_order_next_stage/', move_order_next_stage, name='move_order_next_stage'),
    
    # Fixed URL pattern for delete_business
    path('delete_business/<int:business_id>/', delete_business, name='delete_business'),
    
    # If you want to keep the my_businesses URL
    path('my_businesses/', business, name='my_businesses'),

    # Fixed URL pattern for business_status page
     path('business/<int:business_id>/', business_status, name='business_status'),




     ]
