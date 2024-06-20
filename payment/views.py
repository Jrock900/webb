from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress
from django.contrib import messages


# Create your views here.


def payment_success(request):
    return render(request, "payment_success.html", {})



def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, "checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})

    else:
        shipping_form = ShippingForm(request.POST or None)

        return render(request, "checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})


def billing_info(request):
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})

        else:
            billing_form = PaymentForm()
            return render(request, "billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})



        shipping_form = request.POST
        return render(request, "billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shippingForm})
    else:
        messages.success(request, "Acess Denied")
        return redirect('products:home')


def process_order(request):
    if request.POST:
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        shipping_address = f"{my_shipping['shipping_full_name']}\n{my_shipping['shipping_address1']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        print(shipping_address)
        messages.success(request, "Order Placed")
        return redirect('products:home')

    else:
        messages.success(request, "Acess Denied")
        return redirect('products:home')