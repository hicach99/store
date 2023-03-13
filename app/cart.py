import json
from app.models import Product, Property, Configuration
try:
    config=Configuration.objects.all()[0]
except:
    config=None
class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.session.get('cart')
        if not 'currency' in request.session:
            request.session['currency'] = config.currency.code if config else 'MAD'
        if not self.cart:
            self.cart = {}
            self.session['cart'] = self.cart

    def add(self, product, quantity=1,properties=[]):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]=[{'quantity': quantity,'properties':properties}]
        else:
            if any(x['properties'] == properties for x in self.cart[product_id]):
                index=[i for i,x in enumerate(self.cart[product_id]) if x['properties'] == properties][0]
                self.cart[product_id][index]={'quantity': quantity,'properties':properties}
            else:
                self.cart[product_id].append({'quantity': quantity,'properties':properties})

        self.save()

    def remove(self, product_id, properties=[]):
        if product_id in self.cart:
            index=[i for i,x in enumerate(self.cart[product_id]) if x['properties'] == properties][0]
            self.cart[product_id].pop(index)
            self.save()
    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            for item in self.cart[str(product.id)]:
                properties_ids=item['properties']
                properties = Property.objects.filter(id__in=properties_ids)
                item['product'] = product
                item['properties'] = properties
                item['price'] = float(product.price)
                item['total_price'] = item['price'] * item['quantity']
        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(sum([item['quantity'] for item in item_id]) for item_id in self.cart.values())

    def get_total_price(self):
        return sum(sum([item['total_price'] for item in item_id]) for item_id in self.cart.values())
    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
