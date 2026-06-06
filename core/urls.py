from django.urls import path
from . import views, admin_views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/<int:table_id>/', views.menu, name='menu'),
    path('menu/<int:table_id>/item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('menu/<int:table_id>/item/<int:item_id>/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:table_id>/', views.cart, name='cart'),
    path('cart/<int:table_id>/remove/<int:cart_index>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/<int:table_id>/checkout/', views.checkout, name='checkout'),
    path('orders/<int:table_id>/', views.my_orders, name='my_orders'),
    path('complete/<int:table_id>/', views.complete_session, name='complete_session'),

    # Staff Admin Panel
    path('staff/', admin_views.dashboard, name='staff_dashboard'),
    path('staff/orders/', admin_views.order_list, name='staff_orders'),
    path('staff/orders/<int:order_id>/update/', admin_views.update_order_status, name='update_order_status'),
    path('staff/calls/', admin_views.waiter_calls, name='staff_calls'),
    path('staff/calls/<int:call_id>/resolve/', admin_views.resolve_call, name='resolve_call'),
    path('staff/menu/', admin_views.menu_management, name='staff_menu'),
    path('staff/menu/item/add/', admin_views.menu_item_add, name='menu_item_add'),
    path('staff/menu/item/<int:item_id>/edit/', admin_views.menu_item_edit, name='menu_item_edit'),
    path('staff/tables/', admin_views.table_management, name='staff_tables'),
    path('staff/tables/add/', admin_views.add_table, name='add_table'),
    path('staff/tables/<int:table_id>/status/', admin_views.update_table_status, name='update_table_status'),
]
