from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Add_On(models.Model):
    topping = models.OneToOneField(
       Topping, on_delete=models.CASCADE, related_name="add_on")
   
    def __str__(self):
        return f"{self.topping}"


class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.CASCADE, related_name="items")
    one_price = models.FloatField(blank=True, null=True)
    price_small = models.FloatField(blank=True, null=True)
    price_large = models.FloatField(blank=True, null=True)
    number_toppings = models.IntegerField(blank=True, null=True)
    add_ons = models.BooleanField(default=False)
    extra_cheese = models.BooleanField(default=False)

    def __str__(self):
            return f"{self.name}"


class Order(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="orders")
    date = models.DateTimeField(default=timezone.now)
    price = models.FloatField(blank=True, null=True)

    def __str__(self):
            return f"User: {self.user}, Date: {self.date}"


class Cart(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="cart")
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user}"


class Purchase(models.Model):
    item = models.ForeignKey(
        Item, null=True, on_delete=models.CASCADE, related_name="items")
    SiZE_CHOICES = [
        ("S", "Small"),
        ("L", "Large"),
    ]
    size = models.CharField(max_length=1, choices=SiZE_CHOICES, null=True)
    toppings = models.ManyToManyField(
        Topping, blank=True, related_name="items")
    add_ons = models.ManyToManyField(
        Add_On, blank=True, related_name="items")
    extra_cheese_added = models.BooleanField(default=False)
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total_price = models.FloatField(null=True)
    cart = models.ForeignKey(
        Cart, null=True, on_delete=models.CASCADE, related_name="purchases")
    order = models.ForeignKey(
        Order, null=True, on_delete=models.CASCADE, related_name="purchases")

    def __str__(self):
        return f"{self.item}, {self.size}, {self.toppings}, {self.add_ons}, {self.extra_cheese_added},\
            {self.price}, {self.quantity}, {self.total_price}, {self.cart}, {self.order}"