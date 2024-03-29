import json
from django.http import JsonResponse
from .models import Restaurant, Meal, Order, OrderDetails
from .serializers import RestaurantSerializer, MealSerializer
from django.utils import timezone
from oauth2_provider.models import AccessToken
from django.views.decorators.csrf import csrf_exempt


# ======
#Restaurant
# ======


def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(restaurant=request.user.restaurant,
                                        create_at__gt=last_request_time).count()
    return JsonResponse({"notification": notification})


# ======
#CUSTOMER
# ======

def customer_get_restaurants(request):
    restaurants = RestaurantSerializer(Restaurant.objects.all().order_by("-id"), many=True, context={"request": request}).data
    return JsonResponse({"restaurants": restaurants})


def customer_get_meals(request, restaurant_id):
    meals = MealSerializer(Meal.objects.filter(restaurant_id=restaurant_id).order_by("-id"), many=True, context={"request": request}).data
    return JsonResponse({"meals": meals})


@csrf_exempt
def customer_add_order(request):
    """
    params:
    1. access_token
    2. restaurant_id
    3. address
    4. order_details(json format), example:
        [{"meal_id": 1, "quantity": 2}, {"meal_id": 2, "quantity": 3}]
    return:
    {"status":"success"}
    """

    if request.method == "POST":
        # Get access token
        access_token = AccessToken.objects.get(token=request.POST.get("access_token"), expires__gt=timezone.now())

        # Get customer profile
        customer = access_token.user.customer

        # Check whether customer has any outstanding order
        if Order.objects.filter(customer=customer).exclude(status=Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed."})

        # Check order's address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "address is required"})

        # Get order details
        order_details = json.loads(request.POST["order_details"])

        # Check if meals in only one restaurant and then calculate the order total
        order_total = 0
        for meal in order_details:
            if not Meal.objects.filter(id=meal["meal_id"], restaurant_id=request.POST["restaurant_id"]):
                return JsonResponse({"status": "failed", "error": "meals must be in only one restaurant"})
            else:
                order_total = Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]

        # CREATE ORDER
        if len(order_details) > 0:
            # Step 1 - Create an Order
            order = Order.objects.create(customer=customer, restaurant_id=request.POST["restaurant_id"],
                                         total=order_total,
                                         status=Order.COOKING,
                                         address=request.POST["address"])

            # Step 2 - Create Order Details
            for meal in order_details:
                OrderDetails.objects.create(order=order,
                                            meal_id=meal["meal_id"],
                                            quantity=meal["quantity"],
                                            sun_total=Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"])
                return JsonResponse({"status": "success"})

    return JsonResponse({})


def customer_get_latest_order(request):
    return JsonResponse({})