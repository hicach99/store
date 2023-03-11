from django.urls import path
from app.views import *
urlpatterns = [
    path('', main,name='main'),
    path('product/<slug:slug>', product,name='product_details'),
    path('shop/', products,name='shop'),

    # api calls
    path('api/product/<int:id>', api_product_details,name='api_product_details'),
    path('api/cart', api_cart,name='api_cart'),
    path('api/cart/add', api_add_cart,name='api_add_cart'),
]
