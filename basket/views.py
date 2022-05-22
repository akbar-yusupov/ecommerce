from decimal import Decimal, getcontext

import folium
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

from accounts.models import Address
from store.models import Coupon, Product, Storage

from .basket import Basket
from .utils import get_center_coordinates, get_zoom


class BasketSummaryView(View):
    template_name = "basket/summary.html"

    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        addresses = Address.objects.filter(customer=request.user)
        return render(
            request,
            self.template_name,
            {"basket": basket, "addresses": addresses},
        )

    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        pk = request.POST["address"]
        address = Address.objects.filter(customer=request.user, pk=pk).first()
        if address:
            distances = dict()
            arrival_point = (address.latitude, address.longitude)
            if Storage.objects.filter(country=address.country).exists():
                for storage in Storage.objects.filter():
                    departure_point = (storage.latitude, storage.longitude)
                    distances[storage.pk] = round(
                        geodesic(arrival_point, departure_point).km, 2
                    )
            else:
                for storage in Storage.objects.all():
                    departure_point = (storage.latitude, storage.longitude)
                    distances[storage.pk] = round(
                        geodesic(arrival_point, departure_point).km, 2
                    )
            min_distance_storage = min(distances.items(), key=lambda x: x[1])
            storage = Storage.objects.get(pk=min_distance_storage[0])
            map_ = folium.Map(
                width=1124,
                height=674,
                location=get_center_coordinates(
                    storage.latitude,
                    storage.longitude,
                    address.latitude,
                    address.longitude,
                ),
                min_zoom=4,
                max_bounds=True,
                zoom_start=get_zoom(min_distance_storage[1]),
            )
            folium.Marker(
                (storage.latitude, storage.longitude),
                tooltip=_("Our Storage's location"),
                popup=storage.city,
                icon=folium.Icon(
                    color="purple",
                    icon_color="white",
                    icon="glyphicon glyphicon-cloud",
                ),
            ).add_to(map_)
            folium.Marker(
                (address.latitude, address.longitude),
                tooltip=_("Your address location"),
                popup=address.town_city,
                icon=folium.Icon(
                    color="white",
                    icon_color="green",
                    icon="glyphicon glyphicon-home",
                ),
            ).add_to(map_)
            line = folium.PolyLine(
                locations=(
                    (storage.latitude, storage.longitude),
                    (address.latitude, address.longitude),
                ),
                weight=5,
                color="blue",
            )
            map_.add_child(line)
            title_html = """
                     <head>
                        <style> 
                            html { overflow-y: hidden;  overflow-x: hidden;} 
                        </style>
                    </head>
                """
            map_.get_root().html.add_child(folium.Element(title_html))
            map_ = map_._repr_html_()
            delivery_price = min_distance_storage[1]
            request.session["storage_pk"] = storage.pk
            request.session["delivery_price"] = delivery_price
            request.session.modified = True
            total_price = basket.get_total_price()
            return JsonResponse(
                {
                    "map": map_,
                    "distance": min_distance_storage[1],
                    "customer_city": address.town_city,
                    "storage_city": storage.city,
                    "delivery_price": delivery_price,
                    "total_price": total_price,
                }
            )
        else:
            return redirect("basket:basket_summary")


class BasketAddView(View):
    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        if request.POST.get("action") == "post":
            product_id = int(request.POST.get("product_id"))
            product_qty = int(request.POST.get("product_qty"))
            product = get_object_or_404(Product, id=product_id)
            basket.add(product=product, product_qty=product_qty)
            basket_qty = basket.__len__()
            response = JsonResponse({"qty": basket_qty})
            return response


class BasketUpdateView(View):
    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):

        basket = Basket(request)
        product_id = request.POST.get("product_id")
        product_qty = int(request.POST.get("product_qty"))
        basket.update(product_id, product_qty)
        response = JsonResponse(
            {
                "basket_qty": basket.__len__(),
                "basket_total": basket.get_total_price(),
                "basket_subtotal": basket.get_subtotal_price(),
            }
        )
        return response


class BasketDeleteView(View):
    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        product_id = request.POST.get("product_id")
        basket.delete(product_id)
        response = JsonResponse(
            {
                "basket_qty": basket.__len__(),
                "basket_total": basket.get_total_price(),
                "basket_subtotal": basket.get_subtotal_price(),
            }
        )
        return response
