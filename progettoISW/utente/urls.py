from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
]
