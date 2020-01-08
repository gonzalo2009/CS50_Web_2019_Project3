# The code of this file inside the dotted lines (------------) was extracted from https: // github.com/stripe-samples/card-payment-charges-api and then
# modified.

import os
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topping, Item, Purchase, Category, Cart, Order, Add_On
import json
import stripe

# stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
stripe.api_key = "sk_test_y5XqNCJlrkpnnA8q5DYcwI0m00Icp1n2UT"

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    else:
        return HttpResponseRedirect(reverse("menu"))


def menu_view(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
     
    context = { 
        "items": Item.objects.all(), "categories": Category.objects.all()
    }
    return render(request, "orders/menu.html", context)


def item_view(request, item_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")

    item = Item.objects.get(pk=item_id)
    if request.method == "POST":
        price = 0
        purchase = Purchase(item=item)
        purchase.save()

        if item.number_toppings:
            for i in range(1, item.number_toppings + 1):
                topping_id = request.POST["topping"+str(i)]
                topping = Topping.objects.get(pk=topping_id)
                purchase.toppings.add(topping)

        if item.add_ons:
            for i in range(1, Add_On.objects.all().count() + 1):
                add_on_id = request.POST["add_on"+str(i)]
                if add_on_id != "": 
                    price += 0.5
                    add_on = Add_On.objects.get(pk=add_on_id)
                    purchase.add_ons.add(add_on)

        if item.one_price:
            size=None
            price += item.one_price
        else:
            size = request.POST["size"]
            if size=="S":
                price += item.price_small
                purchase.size = "S"
              
            else:
                price += item.price_large
                purchase.size = "L"
                
        if item.extra_cheese:
            extra_cheese = request.POST["extra_cheese_added"]
            if extra_cheese:
                price += 0.5 
                purchase.extra_cheese_added = True
                
        purchase.price = price
        quantity = request.POST["quantity"]
        purchase.quantity = quantity
        total_price = round(price*float(quantity), 2)
        purchase.total_price = total_price
        cart = request.user.cart
        purchase.cart=cart
        purchase.save()
        total_price_cart = cart.price + purchase.total_price
        cart.price = round(total_price_cart, 2)
        cart.save()
        detail = {"category": str(purchase.item.category), "item": str(purchase.item), 
                  "quantity": str(purchase.quantity), "total_price": str(purchase.total_price)} 
        return JsonResponse(detail)
    
    number_toppings = None

    if item.number_toppings and item.number_toppings > 0:
        number_toppings = range(1, item.number_toppings+1)

    add_on_list = None

    if item.add_ons:
        add_on_list = []
        i = 1
        for j in Add_On.objects.all():
            add_on_list.append({"index": i, "add_on": j})
            i+=1

    context = {
        "item": item, "number_toppings": number_toppings, "toppings": Topping.objects.all(), "add_on_list": add_on_list
    }
    return render(request, "orders/item.html", context)


def cart_view(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    else:
        context = {
            "cart": request.user.cart
        }
        return render(request, "orders/cart.html", context)


def order(r):
    if not r.user.is_authenticated:
        return render(r, "orders/login.html")
    else:
        order = Order(user=r.user)
        cart = r.user.cart        
        order.save()
        purchases = cart.purchases.all()

        for purchase in purchases:          
            purchase.order = order
            purchase.cart = None
            purchase.save()

        order.price = cart.price
        cart.price = 0
        order.save()
        cart.save()
        return order.id
        

def order_view(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    else:  
        order_id = request.POST["order_id"]
        order = Order.objects.get(pk=order_id)
        context = {
            "order": order
        }
        return render(request, "orders/order.html", context)


def order_number_view(request, order_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return render(request, "orders/login.html")
    else:
        order = Order.objects.get(pk=order_id)
        context = {
            "order": order,
        }
        return render(request, "orders/order.html", context)
       
        

def delete_view(request, purchase_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    else:
        cart = request.user.cart
        context = {
            "cart": cart
        }
        price = None

        try:
            purchase = Purchase.objects.get(pk=purchase_id)
            price = cart.price - purchase.total_price 
            cart.price = round(price, 2)
            cart.save()
            purchase.delete()
            detail = {"price": cart.price}
        except KeyError:
            return render(request, "orders/cart.html", context)
        except Purchase.DoesNotExist:
            return render(request, "orders/cart.html", context)
        return JsonResponse(detail)


def orders_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return render(request, "orders/login.html")
    else:
        context = {
            "orders": Order.objects.all()
        }
        return render(request, "orders/orders.html", context)


def get_price_view(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    else:
        return JsonResponse({"price": request.user.cart.price})


def payment_view(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    elif request.method == "POST":
        token = request.POST["token"]
        order_id = order(request)
        order_object = Order.objects.get(pk=order_id) 
        amount = int(order_object.price*100)
        email = order_object.user.email
        
        try:
            charge = stripe.Charge.create(
                amount = amount,
                currency = 'usd',
                source = token,
                receipt_email= email,
                metadata={"order_id":order_id},
            )

            return JsonResponse(charge)
        except stripe.error.CardError as e:
            # Handle "hard declines" e.g. insufficient funds, expired card, etc
            # See https://stripe.com/docs/declines/codes for more
            return JsonResponse({'error': e.user_message})
    else:
        return render(request, "orders/payment.html")   


def register_view(request):
    context = None
    if request.POST: 
        empty_fields=[]

        for x  in dict(request.POST).keys():
            if not request.POST[x]:
                empty_fields.append(x)

        if len(empty_fields)>0:
            context = {"message": "Complete all the fields",
                       "empty_fields": empty_fields}

        elif User.objects.filter(email=request.POST["email"]).exists():
            context = {"message": "The email already exists."}

        elif User.objects.filter(username =  request.POST["username"]).exists():
            context = {"message": "The username already exists."}
            
        elif request.POST["password"] != request.POST["password_confirmation"]:
            context = {"message": "Passwords do not match."}
           
        if context is None:
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = password)
            login(request, user)
            cart=Cart(user=user)
            cart.save()
            return HttpResponseRedirect(reverse("menu"))  
    return render(request, "orders/register.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def login_view(request):
    context = None
    if request.POST:
        empty_fields = []

        for x in dict(request.POST).keys():
            if not request.POST[x]:
                empty_fields.append(x)

        if len(empty_fields) > 0:
            context = {"message": "Complete all the fields",
                       "empty_fields": empty_fields}

        else:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is None:
                context = {"message": "Username or password are incorrect."}

        if context is None:
            login(request, user)
            if not hasattr(request.user, "cart"):
                cart = Cart(user=user)
                cart.save()
            return HttpResponseRedirect(reverse("menu"))

    return render(request, "orders/login.html", context)


def fetch_key_view(request):
    return JsonResponse({"publicKey": "pk_test_GdV8puLK4dimPQxbDT9qLVVs00Pmywpvoo"})
