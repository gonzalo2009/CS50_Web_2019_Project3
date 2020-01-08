from django.contrib import admin

from .models import Topping, Item, Category, Add_On, Order

# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(Add_On)
admin.site.register(Order)



