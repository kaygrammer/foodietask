from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant/', views.restaurant_home, name='restaurant_home'),

    path('restaurant/sign_in', auth_view.LoginView.as_view(template_name='restaurant/sign_in.html'), name='restaurant_sign_in'),
    path('restaurant/sign_out', auth_view.LogoutView.as_view(next_page='/'), name='restaurant_sign_out'),
    path('restaurant/sign_up', views.restaurant_sign_up, name='restaurant_sign_up'),

]
