from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    # web view-restaurant
    path('', views.home, name='home'),
    path('restaurant/', views.restaurant_home, name='restaurant_home'),

    path('restaurant/sign_in', auth_view.LoginView.as_view(template_name='restaurant/sign_in.html'),
         name='restaurant_sign_in'),
    path('restaurant/sign_out', auth_view.LogoutView.as_view(next_page='/'), name='restaurant_sign_out'),
    path('restaurant/sign_up', views.restaurant_sign_up, name='restaurant_sign_up'),

    path('restaurant/account', views.restaurant_account, name='restaurant_account'),

    #meal
    path('restaurant/order', views.restaurant_order, name='restaurant_order'),
    path('restaurant/meal', views.restaurant_meal, name='restaurant_meal'),
    path('restaurant/meal/add', views.restaurant_meal_add, name='restaurant_meal_add'),
    path('restaurant/meal/edit/<int:meal_id>', views.restaurant_meal_edit, name='restaurant_meal_edit'),
    #report
    path('restaurant/report', views.restaurant_report, name='restaurant_report'),

    # APIs

    # path('api/social/', include('rest_framework_social_oauth2.urls')),
]
