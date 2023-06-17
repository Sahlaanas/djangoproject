from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.variantlist, name = 'variantlist'),
    path('addvariant/', views.addvariant, name = 'createvariant'),
    path('editvariant/<int:editvariant_id>/', views.editvariant, name = 'editvariant'),
    path('deletevariant/<int:deletevariant_id>/', views.deletevariant, name='deletevariant')
 
    
    
] 
 