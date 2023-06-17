from django.urls import path
from . import views




urlpatterns = [
    
    path('', views.orderlist, name = 'orderlist'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    
] 
