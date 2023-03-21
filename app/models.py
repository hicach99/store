from django.db import models
from django.utils.text import slugify
from django.db.models import Q
from django.utils.html import mark_safe


class Currency(models.Model):
    code = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255,blank=True)
    def __str__(self):
        return self.code+' : '+self.symbol
    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        self.symbol = self.symbol.upper()
        if not self.symbol:
            self.symbol= self.code
        super(Currency, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Currencies"
class Configuration(models.Model):
    # Website configurations
    website_url = models.CharField(max_length=255,blank=True)
    website_name = models.CharField(max_length=255,null=False)
    logo = models.ImageField(blank=True,upload_to='website_images/')
    logo_white = models.ImageField(blank=True,upload_to='website_images/')
    favicon = models.FileField(blank=True,upload_to='website_images/')
    # SEO configurations
    description = models.TextField()
    keywords = models.TextField()
    author = models.CharField(max_length=255,blank=True)
    # Contact configurations
    support_phone = models.CharField(max_length=255,blank=True)
    contact_phone = models.CharField(max_length=255,blank=True)
    contact_email = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    # Social Meadia configurations
    whatsapp = models.CharField(max_length=255,blank=True)
    instagram = models.CharField(max_length=255,blank=True)
    facebook = models.CharField(max_length=255,blank=True)
    tiktiok = models.CharField(max_length=255,blank=True)
    whatsapp = models.CharField(max_length=255,blank=True)
    # Default Currency
    exchangerate_api=models.CharField(max_length=255,blank=True)
    currency=models.ForeignKey(Currency, on_delete=models.CASCADE)
    currencies=Currency.objects.all()
    # mailing settings
    smtp_host = models.CharField(max_length=255,blank=True)
    smtp_port = models.IntegerField(default=465)
    smtp_username = models.CharField(max_length=255,blank=True)
    smtp_password = models.CharField(max_length=255,blank=True)
    smtp_SSL = models.BooleanField(default=True)
    email_recivers = models.TextField(blank=True)
    # telegram settings
    telegram_bot_api = models.CharField(max_length=255,blank=True)
    telegram_recivers = models.TextField(blank=True)
    # paypal credentials 
    paypal_public_key = models.CharField(max_length=512,blank=True)
    paypal_secret_key = models.CharField(max_length=512,blank=True)
    paypal_sandbox = models.BooleanField(default=False)
    # paypal credentials 
    cmi_merchant_id = models.CharField(max_length=512,blank=True)
    cmi_secret_key = models.CharField(max_length=512,blank=True)
    cmi_sandbox = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.website_name
    def get_telegram_recivers(self):
        return [r.strip() for r in self.telegram_recivers.split(',')]
    def get_email_recivers(self):
        return [r.strip() for r in self.email_recivers.split(',')]
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,null=True)
    image = models.ImageField(upload_to='category_images/',blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    @staticmethod
    def get_all():
        return Category.objects.all()
    class Meta:
        verbose_name_plural = "Categories"
class PropertyType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Property(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100,null=True)
    type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.name
        super(Property, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Properties"
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
class Product(models.Model):
    product_status = [
        ('Hot', 'Hot'),
        ('Sale', 'Sale'),
        ('New', 'New'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,null=True)
    status=models.CharField(max_length=255,choices=product_status,default='New')
    description = models.TextField(blank=True)
    product_details = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    properties = models.ManyToManyField(Property)
    tags = models.ManyToManyField(Tag)
    enabled=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        ordering = ['-created_at']
    def img_preview(self): #new
        return mark_safe(f'<img src = "{self.images.all()[0].url}" width = "300"/>')
    def get_images(self):
        return self.images.all()
    def get_statistics(self):
        rates=[r.rating for r in self.reviews.all()]
        return len(rates),int(sum(rates)/len(rates)) if len(rates)>=1 else 0
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    # Get products by category
    @staticmethod
    def get_by_category(slug):
        try:
            category=Category.objects.get(slug=slug)
            return category.products.all()
        except:
            return []
    # Get products by tag
    @staticmethod
    def get_by_tag(slug):
        data=[]
        try:
            products=Product.objects.all()
            tag=Tag.objects.get(slug=slug)
            for product in products:
                if product.tags.all().contains(tag): data.append(product)
            return data
        except:
            return []
    # Get products by query
    def get_by_query(q):
        words=q.split()
        products=[]
        try:
            for word in words:
                for p in Product.objects.filter(Q(name__icontains=word)):
                    if not p.id in [i.id for i in products]: products.append(p)
            return products
        except:
            return []
    # Get products ordered by price
    @staticmethod
    def get_by_price(products=[],desc=True):
        return sorted(products, key=lambda x: x.price, reverse=desc)
    # Get products ordered by date
    @staticmethod
    def get_by_date(products=[],desc=True):
        return sorted(products, key=lambda x: x.created_at.timestamp(), reverse=desc)
    # Get products ordered by rating
    @staticmethod
    def get_by_rating(products=[]):
        for product in products:
            product.rating=product.get_statistics()[1]
        return sorted(products, key=lambda x: x.rating, reverse=True)
    @staticmethod
    def get_products(request):
        products=None
        if 'category' in request.GET:
            products=Product.get_by_category(slug=request.GET['category'])
        elif 'tag' in request.GET:
            products=Product.get_by_tag(slug=request.GET['tag'])
        elif 'q' in request.GET:
            products=Product.get_by_query(q=request.GET['q'])
        else:
            products=Product.objects.all()
        if 'orderby' in request.GET:
            if request.GET['orderby']=='price-desc':
                products=Product.get_by_price(products=products)
            if request.GET['orderby']=='price':
                products=Product.get_by_price(products=products,desc=False)
            if request.GET['orderby']=='rating':
                products=Product.get_by_rating(products=products)
            if request.GET['orderby']=='latest':
                products=Product.get_by_date(products=products)
            if request.GET['orderby']=='oldest':
                products=Product.get_by_date(products=products,desc=False)
        return products
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        return f"{self.product.name} Image"
    
class ProductInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='informations')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    def __str__(self):
        return '{"'+str(self.key)+'":"'+str(self.value)+'"}'

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=1)
    title = models.CharField(max_length=255,default='')
    content = models.TextField(blank=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    token = models.CharField(blank=True,max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=255)
    address = models.TextField(null=True)
    city = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255,null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    complete = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    class Meta:
        ordering = ['-date_ordered']
    def calculate_total_price(self):
        items=self.items.all()
        self.total_price=sum([item.total_price for item in items])
        self.save()
    def __str__(self):
        return str(self.id)
    @staticmethod
    def create_order(info,cart):
        if len(cart)>0:
            order = Order.objects.create(token=info['paypal_order_id'],complete=True,payment_method=info['payment_method'],name=info['name'],phone=info['phone'],email=info['email'],address=info['address'],city=info['city']) if 'paypal_order_id' in info else Order.objects.create(payment_method=info['payment_method'],name=info['name'],phone=info['phone'],email=info['email'],address=info['address'],city=info['city'])
            order.save()
            order=Order.objects.get(id=order.id)
            for item_id in cart:
                for item in item_id:
                    properties = item['properties']
                    order_item=OrderItem.objects.create(order=order,product=item['product'],quantity=item['quantity'])
                    for properity in properties: order_item.properties.add(properity)
                    order_item.save()
            order.calculate_total_price()
            cart.clear()
            return order
        return None
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    properties = models.ManyToManyField(Property)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    def save(self, *args, **kwargs):
        self.total_price= self.quantity * self.product.price
        super(OrderItem, self).save(*args, **kwargs)

