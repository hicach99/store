from django.db import models
from django.utils.text import slugify

class Configuration(models.Model):
    # Website configurations
    website_url = models.CharField(max_length=255,default='.')
    website_name = models.CharField(max_length=255,null=False)
    # SEO configurations
    description = models.TextField()
    keywords = models.TextField()
    author = models.CharField(max_length=255,default='.')
    # Contact configurations
    support_phone = models.CharField(max_length=255,default='.')
    contact_phone = models.CharField(max_length=255,default='.')
    contact_email = models.CharField(max_length=255,default='.')
    address = models.CharField(max_length=255,default='.')
    # Social Meadia configurations
    whatsapp = models.CharField(max_length=255,default='.')
    instagram = models.CharField(max_length=255,default='.')
    facebook = models.CharField(max_length=255,default='.')
    tiktiok = models.CharField(max_length=255,default='.')
    whatsapp = models.CharField(max_length=255,default='.')
    def __str__(self) -> str:
        return self.website_name

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
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
class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

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
    tags = models.ManyToManyField(Tag)
    properties = models.ManyToManyField(Property)
    enabled=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        ordering = ['-created_at']
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
    # Get products ordered by price
    @staticmethod
    def get_by_price(desc=True):
        d = '-' if desc else ''
        return Product.objects.order_by(d+'price')
    # Get products ordered by date
    @staticmethod
    def get_by_date(limit=None,desc=True):
        d = '-' if desc else ''
        return Product.objects.order_by(d+'created_at')

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