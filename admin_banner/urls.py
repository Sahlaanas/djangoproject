from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.bannerlist, name = 'bannerlist'),
    path('addbanner/', views.addbanner, name = 'addbanner'),
    path('editbanner/<int:editbanner_id>/', views.editbanner, name = 'editbanner'),
    path('deletebanner/<int:deletebanner_id>/', views.deletebanner, name='deletebanner')
 
    
    
] 
 