from django.urls import path,re_path
from .  import views





urlpatterns = [
    path('', views.myOrders, name = 'myOrders'),
    path('orderView/<str:t_no>/', views.orderview, name='orderview'),
    path('myorders/user_order_track/<int:id>/', views.user_order_track, name='user_order_track'),

    path('ordercancel/', views.ordercancel, name='ordercancel')
]
    
  
    

    
   
    
    
    
    
    
