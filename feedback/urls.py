from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('submit/<int:table_id>/<int:order_id>/', views.submit_feedback, name='submit_feedback'),
]
