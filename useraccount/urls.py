from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('forgetpassword/', views.forgetpassword, name = 'forgetpassword'),
    path('resetpassword/', views.resetpassword, name = 'resetpassword'),
    path('mobile_login/', views.mobile_login, name = 'mobile_login'),
    path('otp/<uid>/', views.otp, name = 'otp')
]
