from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.brandlist, name = 'brandlist'),
    path('createbrand/', views.createbrand, name = 'createbrand'),
    path('editbrand/<slug:editbrand_slug>/', views.editbrand, name = 'editbrand'),
    path('deletebrand/<slug:deletebrand_slug>/', views.deletebrand, name = 'deletebrand'),
    
    
    path('categorylist/', views.categorylist, name='categorylist'),
    path('createcategory/', views.createcategory, name = 'createcategory'),
    path('editcategory/<slug:editcategory_slug>/', views.editcategory, name = 'editcategory'),
    path('deletecategory/<slug:deletecategory_slug>/', views.deletecategory, name = 'deletecategory'),
    
    
    path('userlist/', views.userlist, name = 'userlist'),  
    path('blockunblock/<int:id>/', views.blockUnblock, name='blockunblock'),
    
    
    
    
    
    
    
    
    
    
] 
