from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('store/<str:cat_slug>/<str:prod_slug>/', views.productview, name = 'productview'),
 
   
]
