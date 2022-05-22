from decimal import Decimal

from django.conf import settings

from store.models import Product


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, product_qty):
        product_id = product.id
        if product_id in self.basket:
            self.basket[product_id]["qty"] = product_qty
        else:
            product.final_price = product.regular_price - (
                product.regular_price / 100 * product.discount_percentage
            )
            self.basket[product_id] = {
                "price": str(product.final_price),
                "qty": product_qty,
            }

        self.save()

    def update(self, product_id, product_qty):
        if product_id in self.basket:
            self.basket[str(product_id)]["qty"] = product_qty
            self.save()

    def delete(self, product_id):
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        return sum(item["qty"] for item in self.basket.values())

    def get_subtotal_price(self):
        return sum(
            Decimal(item["price"]) * item["qty"]
            for item in self.basket.values()
        )

    def get_total_price(self):
        subtotal = self.get_subtotal_price()
        total = subtotal + Decimal(self.session["delivery_price"])
        return round(total, 2)

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        if self.session.get("delivery_price", None):
            del self.session["delivery_price"]
        if self.session.get("storage_pk", None):
            del self.session["storage_pk"]
        if self.session.get("coupon_discount", None):
            del self.session["coupon_discount"]
        self.save()
