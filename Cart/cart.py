from Marcetplace2 import settings
from Vendor.models import Product
from decimal import Decimal


class Cart():
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = {}
            self.session[settings.CART_SESSION_ID] = cart
        self.cart = cart

    def add_product(self,product,quantity=1 ,overrider_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0,'price':str(product.price)}
        if overrider_quantity:
            self.cart[product_id]['quantity']=quantity
        else:
            self.cart[product_id]['quantity']+=quantity
        self.save()
    def save(self):
        self.session.modified = True

    def remove_product(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for itemt in cart.values():
            itemt['price'] = float(Decimal(itemt['price']))
            itemt['total_price'] = float(itemt['price'] * itemt['quantity'])
            yield itemt

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def total_price(self):
        return float(sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()))

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

