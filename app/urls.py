from django.urls import path
from app.views import *
urlpatterns = [
    path('', main,name='main'),
    path('product/<slug:slug>', product,name='product_details'),
    path('shop/', products,name='shop'),
    path('cart/', cart,name='cart'),
    path('checkout/', checkout,name='checkout'),
    path('cart/remove', remove_cart,name='remove_cart'),
    path('cart/update', update_cart,name='update_cart'),
    path('cart/clear', clear_cart,name='clear_cart'),
    path('order/checkout_process', checkout_process,name='checkout_process'),
    path('order/success', success,name='success'),
    path('order/echec', echec,name='echec'),
    # session: currency, language
    path('set_currency/<str:code>', set_currency,name='set_currency'),
    # api calls
    path('api/product/<int:id>', api_product_details,name='api_product_details'),
    path('api/cart', api_cart,name='api_cart'),
    path('api/cart/add', api_add_cart,name='api_add_cart'),
    path('api/order/create', api_create_order,name='api_create_order'),
    path('test', test,name='test'),
]
