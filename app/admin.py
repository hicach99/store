

from django.contrib import admin
from app.forms import ConfigurationAdminForm, OrderAdminForm, ProductAdminForm, PropertyAdminForm
from .models import *

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3
class InfoInline(admin.TabularInline):
    model = ProductInformation
    extra = 1
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
class ConfigurationAdmin(admin.ModelAdmin):
    list_display=('id','website_name')
    form = ConfigurationAdminForm
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name')
    exclude = ('slug',)
class TagAdmin(admin.ModelAdmin):
    display=('name')
    exclude = ('slug',)
class CurrencyAdmin(admin.ModelAdmin):
    list_display=('code','symbol')
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','price','old_price')
    readonly_fields = ['img_preview']
    form = ProductAdminForm
    exclude = ('slug',)
    inlines = [ImageInline,InfoInline]
class ProductReviewAdmin(admin.ModelAdmin):
    list_display=('id','title','product','name')

class PropertyAdmin(admin.ModelAdmin):
    list_display=('id','name','value','type')
    form = PropertyAdminForm
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','name','phone','total_price','complete')
    form = OrderAdminForm
    inlines = [OrderItemInline]

admin.site.register(Configuration,ConfigurationAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Property,PropertyAdmin)
admin.site.register(PropertyType)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Currency,CurrencyAdmin)
admin.site.register(Order,OrderAdmin)
