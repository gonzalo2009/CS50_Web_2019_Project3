# Project 3

Web Programming with Python and JavaScript

-base.html: contains the basic layout of the pages.

-register.html: this page is where tou register as a user, compliting the form.

-login.htmml: once you have registered, on this page you register as a user.

-menu: once you have logged in you will be redirected to this page. Here you can view all the items of the menu with their prices. If you click the blue button at the right of an item you will be redirected the page of the item.

-item.html: this page coitains the detail of the item that you have choosed in the menu page. Here you can choose the size (small or large), the quantity, the toppings, the add ons and if you want to add extra cheese to add to the cart clicking the blue button. Once you have clicked the blue button adding the item you will be asked if you want to continue shopping (go back to the menu) or go to the cart.

-cart.html: here you can view all the items that you have added to your cart. You can delete an item by clicking the gray button at the right of the item and you can go to payment page by clicking the blue button to pay. 

-payment.html*: Here you have to pay (through the stripe API) providing the information of a credit card. Once you submit the information the                 order will be placed and you will be redirected to the page of the order.

-order.html: after the payment you will be redirected to this page. Here you can view all the detail of the order that you have made.

-orders.html: you have access to this page if you are logged in as an administrator. To go to this page you have to click the link in the                   upper left corner. Here you can view a table with all the orders with the id and the date the order was placed, and you can the blue button at the right of an order to go to the page of that order.

-views.py: contains the code in python to make interactions between the database and the client's browser.

-models.py: Contains the code of the classes. There are 7 classes: Topping, Add_On, Category, item, Order, Cart and Purchase.  

-scripts.js*: contains the code in javascript that runs on the client side and  make changes to the html files and ask and send information to the server  

-styles.css: contains the code to set the style to all the html files.

-global.css* and normalize.css*: contains the code to the style to the payment.html files.

-icon.png*: contains the image for the favicon of the website.

LICENSE*: is the license to use the code extracted from https://github.com/stripe-samples/card-payment-charges-api.

Personal Touch: The web application is integrated with the Stripe Api.

"Special" pizza: consist in a pizza that contains five toppings to choose.

* Those are files extracted from the web or files that contains code extracted from the web:
    
    icon.png: image from https://i.pinimg.com/originals/b5/3c/54/b53c54112aecb87f5ee59862af1fbc93.png.

    payment.html, global.css* and normalize.css*: those files were extrated from https://github.com/stripe-samples/card-payment-charges-api and then modified. 

    scripts.js, views.py: contains code extracted from https://github.com/stripe-samples/card-payment-charges-api and then modified. The lines of code extracted are specified in each file. 

    LICENSE: license from https://github.com/stripe-samples/card-payment-charges-api.