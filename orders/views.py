from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from accounts.models import Address
from basket.basket import Basket
from store.models import Storage

from .models import Order, OrderItem


class OrderListView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        orders = user_orders(request)
        return render(request, "orders/list.html", {"orders": orders})


class AddOrderView(View):
    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        if request.POST.get("action") == "add":
            basket = Basket(request)
            order_key = request.POST["order_key"]
            address = Address.objects.get(pk=request.POST["address_pk"])
            storage = Storage.objects.get(pk=request.POST["storage_pk"])
            coupon = request.session.get("coupon_discount", 0)
            total_price = basket.get_total_price()
            total_price = total_price - total_price * coupon / 100

            if not Order.objects.filter(order_key=order_key).exists():
                print("BASKET", basket)
                order = Order.objects.create(
                    address=address,
                    storage=storage,
                    total_paid=total_price,
                    order_key=order_key,
                )
                for item in basket:
                    OrderItem.objects.create(
                        order_id=order.pk,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["qty"],
                    )
                response = JsonResponse({"success": "True"})
                return response
        raise Http404


def payment_confirmation(order_key):
    Order.objects.filter(order_key=order_key).update(billing_status=True)


def user_orders(request):
    orders = Order.objects.filter(
        address__customer__id=request.user.id
    ).filter(billing_status=True)
    return orders
