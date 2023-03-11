import json

from app.models import Product, Property

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.session.get('cart')
        if not self.cart:
            self.cart = {}
            self.session['cart'] = self.cart

    def add(self, product, quantity=1,properties=[]):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['properties'] = properties
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price),'properties':properties}

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            properties_ids=self.cart[str(product.id)]['properties']
            properties = Property.objects.filter(id__in=properties_ids)
            self.cart[str(product.id)]['product'] = product
            self.cart[str(product.id)]['properties'] = properties
        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
