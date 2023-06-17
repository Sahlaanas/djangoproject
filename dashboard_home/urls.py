from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.admin_home, name = 'admin_home'),
    path('admin_login/', views.admin_login, name = 'admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_sales/', views.admin_sales, name='salesreport')
    
] 
