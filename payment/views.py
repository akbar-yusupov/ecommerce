import json

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Address
from basket.basket import Basket
from orders.views import payment_confirmation
from store.models import Storage


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect("store:store_home")

    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        total_price = basket.get_total_price()
        storage_pk = request.session["storage_pk"]
        coupon = request.session.get("coupon_discount", 0)
        delivery = request.session["delivery_price"]
        address_pk = request.POST["address"]
        if (
            Storage.objects.filter(pk=storage_pk).exists()
            and delivery
            and Address.objects.filter(
                pk=address_pk, customer=self.request.user
            ).exists()
        ):
            total = str(total_price - total_price * coupon / 100)
            total = total.replace(".", "")
            total = int(total)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.create(
                amount=total,
                currency="USD",
                metadata={"userid": request.user.id},
            )
            total_price = basket.get_total_price()
            total_price = total_price - total_price * coupon / 100

            return render(
                request,
                "payment/payment_form.html",
                {
                    "client_secret": intent.client_secret,
                    "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
                    "storage_pk": storage_pk,
                    "address_pk": address_pk,
                    "total_price": total_price,
                },
            )
        else:
            return redirect("store:store_home")


class OrderPlacedView(View):
    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        basket.clear()
        return render(request, "payment/order_placed.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    if event.type == "payment_intent.succeeded":
        print("HANDLED payment_intent.succeeded")
        payment_confirmation(event.data.object.client_secret)
    else:
        print(f"Unhandled event type {event.type}")

    return HttpResponse(status=200)
