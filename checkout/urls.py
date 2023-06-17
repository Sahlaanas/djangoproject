from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name = 'checkout'),
    path('place-order/', views.placeorder, name = 'placeorder'),
    path('proceed-to-pay/', views.razorpaycheck, name = 'razorpaycheck'),
 
   
]
