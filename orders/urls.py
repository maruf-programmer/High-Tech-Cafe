from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('waiter/<int:table_id>/', views.call_waiter, name='call_waiter'),
    path('complete/<int:order_id>/', views.mark_order_completed, name='mark_order_completed'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('payment/<int:order_id>/process/', views.process_payment, name='process_payment'),
]
