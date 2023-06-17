from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.productlist, name = 'productlist'),
    path('createproduct/', views.createproduct, name = 'createproduct'),
    path('deleteproduct/<str:prod_slug>/', views.deleteproduct, name='deleteproduct'),    
    path('editproduct/<str:prod_slug>', views.editproduct, name='editproduct'),
    
    
    path('couponlist/', views.couponlist, name = 'couponlist'),
    path('addcoupon/', views.addcoupon, name = 'addcoupon'),
    path('deletecoupon/<int:deletecoupon_id>/', views.deletecoupon, name = 'deletecoupon'),
    path('editcoupon/<int:editcoupon_id>/', views.editcoupon, name='editcoupon'),
    
] 
 