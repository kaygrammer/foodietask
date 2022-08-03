from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, RestaurantForm, AccountForm, MealForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Meal, OrderDetails, Order


def home(request):
    context = {}
    return redirect(restaurant_home)


@login_required(login_url='/restaurant/sign_in')
def restaurant_home(request):
    return redirect(restaurant_order)


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


#account
@login_required(login_url='/restaurant/sign_in')
def restaurant_account(request):
    account_form = AccountForm(instance=request.user)
    restaurant_form = RestaurantForm(instance=request.user.restaurant)

    if request.method == "POST":
        account_form = AccountForm(request.POST, instance=request.user)
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance=request.user.restaurant)

        if account_form.is_valid() and restaurant_form.is_valid():
            account_form.save()
            restaurant_form.save()
    
    context = {"account_form": account_form, "restaurant_form": restaurant_form}
    return render(request, 'restaurant/account.html', context)


#Meals
@login_required(login_url='/restaurant/sign_in')
def restaurant_meal(request):
    meals = Meal.objects.filter(restaurant=request.user.restaurant).order_by("-id")
    context = {"meals": meals}
    return render(request, 'restaurant/meal.html', context)


@login_required(login_url='/restaurant/sign_in')
def restaurant_meal_add(request):
    meal_form = MealForm()

    if request.method == "POST":
        meal_form = MealForm(request.POST, request.FILES)

        if meal_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.restaurant = request.user.restaurant
            meal.save()
            return redirect(restaurant_meal)

    context = {"meal_form": meal_form}
    return render(request, 'restaurant/add_meal.html', context)


@login_required(login_url='/restaurant/sign_in')
def restaurant_meal_edit(request, meal_id):
    meal_form = MealForm(instance=Meal.objects.get(id=meal_id))

    if request.method == "POST":
        meal_form = MealForm(request.POST, request.FILES, instance=Meal.objects.get(id=meal_id))

        if meal_form.is_valid():
            meal_form.save()
            return redirect(restaurant_meal)

    context = {"meal_form": meal_form}
    return render(request, 'restaurant/edit_meal.html', context)


#restaurant
@login_required(login_url='/restaurant/sign_in')
def restaurant_order(request):
    if request.method == "POST":
        order = Order.objects.get(id=request.POST["id"])
        if order.status == Order.COOKING:
            order.status = Order.READY
            order.save()

    orders = Order.objects.filter(restaurant=request.user.restaurant).order_by("-id")
    context = {"orders": orders}
    return render(request, 'restaurant/order.html', context)


@login_required(login_url='/restaurant/sign_in')
def restaurant_report(request):
    context = {}
    return render(request, 'restaurant/report.html', context)
