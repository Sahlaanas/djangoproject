from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.offerlist, name = 'offerlist'),
    path('addoffer/', views.addoffer, name = 'addoffer'),
    path('editoffer/<int:editoffer_id>/', views.editoffer, name = 'editoffer'),
    path('deleteoffer/<int:deleteoffer_id>/', views.deleteoffer, name='deleteoffer'),
 
    
    
] 
