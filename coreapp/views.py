from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, RestaurantForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def home(request):
    context = {}
    return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign_in')
def restaurant_home(request):
    context = {}
    return render(request, 'restaurant/home.html', context)


def restaurant_sign_up(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            ))
            return redirect(restaurant_home)

    context = {'user_form': user_form, 'restaurant_form': restaurant_form}
    return render(request, 'restaurant/sign_up.html', context)