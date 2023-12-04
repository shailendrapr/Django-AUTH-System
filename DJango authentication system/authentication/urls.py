from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

from authentication import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    #path('activate/<uidb64>/token',views.activate,name="activate"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate')


    

]
