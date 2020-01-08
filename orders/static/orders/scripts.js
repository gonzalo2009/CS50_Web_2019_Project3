// The code of this file inside the dotted lines (------------) was extracted from https: // github.com/stripe-samples/card-payment-charges-api and then
// modified. 
window.onload = () => {
    modal_add = document.querySelector("#modal-add");
    modal_confirm = document.querySelector("#modal-confirm");
    set_price()
    add_item();
    change_modal();
    delete_purchase();
    place_order();
    payment();
    confirm_payment();
    watch_form()
};

function change_price_selection(price_selection, quantity){
    total_price = 0
    
    if (price_selection){
        price = parseFloat(price_selection.options[price_selection.selectedIndex].dataset.price);
        total_price += price
    }

    else{
        one_price = document.querySelector("#total-price");
        price = parseFloat(one_price.dataset.price);
        total_price += price
    }

        document.querySelectorAll(".form-check-input").forEach(check_box => {
            if (check_box.checked == true){
                total_price += 0.5
            }
        });
        
    total_price *=quantity.value;
    total_price = (total_price).toFixed(2);

    if(!isNaN(total_price)){
        document.querySelector("#total-price").innerHTML = `total price: ${total_price}`;
    }
    else
        document.querySelector("#total-price").innerHTML = `total price:`;
}


function add_item(){
    if (document.title == "Add to cart") {
        form = document.querySelector("form");
        form.onsubmit = event => {
            event.preventDefault();
            completed = true;
            document.querySelectorAll("select, input").forEach(input => {
                if (!input.value) {
                    input.style.borderColor = "red"
                    completed = false;
                }
            });

            if (completed) {
                data = new FormData();
                document.querySelectorAll("select, input").forEach(detail => {
                    if (detail.type == "checkbox" && detail.checked == false)
                        data.append(detail.getAttribute("name"), "")
                    
                    else
                        data.append(detail.getAttribute("name"), detail.value)
                });
                url = document.querySelector("#detail").dataset.url;
                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: data
                }).then(function (result) {
                    return result.json(); 
                }).then(function (data) {
                    modal_add.querySelector(".item").innerHTML = `<h5>Category: ${data["category"]}</h5>
                                                <h5>Item: ${data["item"]}</h5>
                                                <h5>Quantity: ${data["quantity"]}</h5>
                                                <h5>Total Price: ${data["total_price"]}</h5>`;
                });
                modal_add.style.display = "block";
            }
            else
                alert("Complete all the fields")
        }
    }
}

function delete_purchase(){
     document.querySelectorAll(".delete-purchase").forEach(button => {
         button.onclick = e =>{
             request = new XMLHttpRequest();
             url = button.dataset.url;
             request.open('GET', url);
             request.onload = () => {
                 if (document.querySelectorAll(".delete-purchase").length==1){
                     cart_container = document.querySelector("#url_menu_id")
                     url = cart_container.dataset.url
                     cart_container.innerHTML = `<h1 class="center-header">Shoppping Cart</h1>
                                                 <h2 class="center-header">The cart is empty. Go to <a href ="${url}">menu</a>.</h2>`;
                 }

                 else{
                    e.target.parentElement.parentElement.remove();
                    detail = JSON.parse(request.responseText);
                    price=detail["price"]
                    document.querySelector("#total-price-cart").innerHTML = `Total price: ${price}` 
                 }
                 location.hash=document.querySelector("#col-8").innerHTML;
             };    
             request.send()
         }
     });
}

function place_order() {
    button = document.querySelector("#order")
    if(button)
        button.onclick = () => {
            modal_confirm.style.display = "block";
    }
}

function set_price() {
    if (document.title == "Add to cart") {
        price_selection = document.querySelector("#price-selection");
        quantity = document.querySelector("#quantity");

        if (price_selection) 
            price_selection.onchange = () => {
                change_price_selection(price_selection, quantity)
            }
          
        document.querySelectorAll(".form-check-input").forEach(check_box => {
            check_box.onchange = () => {
                change_price_selection(price_selection, quantity)
            }
        });
        
        
        document.querySelector("#quantity").onchange = () => {
            change_price_selection(price_selection, quantity)
        }
    }

}

function confirm_payment() {
    if (document.title == "Shopping Cart") {
        button_confirm_payment = document.querySelector("#button-confirm-payment")

        if (button_confirm_payment)
            button_confirm_payment.onclick = () => {
            cart_container = document.querySelector("#url_menu_id")
            modal_confirm.style.display = "none";
            cart_container.innerHTML = `<h1 class="center-header">Shoppping Cart</h1>
                                        <h2 class="center-header">The cart is empty. Go to <a href="${cart_container.dataset.url}">menu</a>.</h2>`
        }
    }
}


function change_modal(){
    document.querySelectorAll(".modal").forEach(modal => {
        modal.querySelector(".close").onclick = () => {
            modal.style.display = "none";
        }

        window.onclick = e => {
            if (e.target == modal) {
                modal.style.display = "none";
            }
        }

        if (document.querySelector("#cancel"))
            document.querySelector("#cancel").onclick = () => {
                modal.style.display = "none";
        }
    });
}


function watch_form() {
    if (document.title == "Register" || document.title == "Login") {
        context_message = document.querySelector("#context-message");
        context_fields = document.querySelector("#context-fields");

        if (context_fields) {
            document.querySelectorAll("select, input").forEach(detail => {
                if (context_fields.dataset.fields.includes(detail.name)) {
                    detail.style.borderColor = "red"
                }
            });
        }

        if (context_message) {
            message = context_message.dataset.message;
            alert(message);
        }
    }
}

// ------------------------------------------------------------------------------------------------------------------------------
function payment(){
    if (document.title == "Payment") {
        url_key = document.querySelector("#payment").dataset.url_key
        payment_form = document.querySelector("#payment-form")
        order_data = new FormData();
        
        // A reference to Stripe.js
        var stripe;

        // Disable the button until we have Stripe set up on the page
        document.querySelector("button").disabled = true;
        
        fetch(url_key)
            .then(function (result) {
                return result.json();
            })
            .then(function (data) {
                return setupElements(data);
            })
            .then(function ({ stripe, card, clientSecret }) {
                document.querySelector("button").disabled = false;

                payment_form.addEventListener("submit", function (event) {
                    event.preventDefault();
                    pay(stripe, card, clientSecret);
                });
            });

        var setupElements = function (data) {
            stripe = Stripe(data.publicKey);
            /* ------- Set up Stripe Elements to use in checkout form ------- */
            var elements = stripe.elements();
            var style = {
                base: {
                    color: "#32325d",
                    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                    fontSmoothing: "antialiased",
                    fontSize: "16px",
                    "::placeholder": {
                        color: "#aab7c4"
                    }
                },
                invalid: {
                    color: "#fa755a",
                    iconColor: "#fa755a"
                }
            };
            var card = elements.create("card", { style: style });
            card.mount("#card-element");

            return {
                stripe: stripe,
                card: card,
                clientSecret: data.clientSecret
            };
        };

        /*
         * Collect card details and pay for the order
         */
        var pay = function (stripe, card) {
            changeLoadingState(true);

            // Create a token with the card details
            stripe
                .createToken(card)
                .then(function (result) {
                    if (result.error) {
                        showError(result.error.message);

                    } else {
                        order_data.append("token", result.token.id)
                        payment_url = document.querySelector("#payment_url").dataset.url
                        return fetch(payment_url, {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": getCookie("csrftoken") 
                            },
                            body: order_data
                        });
                    }
                })
                .then(function (result) {
                    return result.json();
                })
                .then(function (paymentData) {
                    if (paymentData.error) {
                        // The card was declined by the bank
                        // Show error and request new card
                        showError(paymentData.error);
                    } else {
                        orderComplete(paymentData);
                    }
                });
        };
        /* ------- Post-payment helpers ------- */
        /* Shows a success / error message when the payment is complete */
        var orderComplete = function (charge) {

            order_id = charge["metadata"]["order_id"]
            send_form = document.querySelector("#send-form")
            send_form.innerHTML = `<input name="csrfmiddlewaretoken" type="text" value=${getCookie("csrftoken")}>
                                   <input name="order_id" type="text" value=${order_id}>`
                    
            changeLoadingState(false);
            send_form.submit(); 
        };

        var showError = function (errorMsgText) {
            changeLoadingState(false);
            var errorMsg = document.querySelector(".sr-field-error");
            errorMsg.textContent = errorMsgText;
            setTimeout(function () {
                errorMsg.textContent = "";
            }, 4000);
        };

        // Show a spinner on payment submission
        var changeLoadingState = function (isLoading) {
            if (isLoading) {
                document.querySelector("button").disabled = true;
                document.querySelector("#spinner").classList.remove("hidden");
                document.querySelector("#button-text").classList.add("hidden");
            } else {
                document.querySelector("button").disabled = false;
                document.querySelector("#spinner").classList.add("hidden");
                document.querySelector("#button-text").classList.remove("hidden");
            }
        };
    }
}
// -----------------------------------------------------------------------------------------------------------------------------------

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
