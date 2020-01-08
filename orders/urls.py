from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu", views.menu_view, name="menu"),
    path("menu/<int:item_id>", views.item_view, name="item"),
    path("cart", views.cart_view, name="cart"),
    path("order", views.order_view, name="order"),
    path("order/<int:order_id>", views.order_number_view, name="order_number"),
    path("delete/<int:purchase_id>", views.delete_view, name="delete"),
    path("orders", views.orders_view, name="orders"),
    path("payment", views.payment_view, name="payment"),
    path("get_price", views.get_price_view, name="get_price"),
    path("fetch_key", views.fetch_key_view, name="fetch_key")
    
]
