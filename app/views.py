import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from app.cart import Cart
from app.models import *
from django.template.loader import render_to_string

from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from urllib.parse import unquote, urlparse
# Loading Configuration
try:
    config=Configuration.objects.all()[0]
except:
    config=None

def set_currency(request,code:str):
    request.session['currency']=code
    try:
        view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
    except Resolver404:
        view = None
    if view:
        args=view.args
        kwargs=json.loads(unquote(str(view.kwargs).replace("'",'"')))
        next_url = reverse(view.url_name, args=args, kwargs=kwargs)
        response = HttpResponseRedirect(next_url)
    else:
        response = redirect("main")
    return response

def main(request):
    latest_products=Product.objects.all()
    cart = Cart(request)
    categories=Category.get_all()
    return render(
        request,
        'index.html',
        {
            'config':config,
            'cart':cart,
            'categories':categories,
            'latest_products':latest_products
        }
    )
def product(request,slug):
    cart = Cart(request)
    product = Product.objects.get(slug=slug)
    categories=Category.get_all()
    related_products=Product.objects.all()
    return render(
        request,
        'product.html',
        {
            'config':config,
            'cart':cart,
            'categories':categories,
            'related_products':related_products,
            'product':product,
        }
    )
def products(request):
    cart = Cart(request)
    categories=Category.get_all()
    products=Product.get_products(request=request)
    return render(
        request,
        'shop.html',
        {
            'config':config,
            'cart':cart,
            'categories':categories,
            'products':products,
        }
    )
def cart(request):
    cart = Cart(request)
    categories=Category.get_all()
    return render(
        request,
        'cart.html',
        {
            'config':config,
            'cart':cart,
            'categories':categories,
        }
    )

# api calls
def api_product_details(request,id):
    try:
        product=Product.objects.get(id=id)
        html=render_to_string('components/commun/product_modal_content.html',{'product':product},request=request)
        data={
            'status' : 'ok',
            'html': html
        }
    except Exception as e:
        data={
            'status':'error',
            'message':e
        }
    return JsonResponse(data,safe=False,json_dumps_params={"ensure_ascii": False})
def api_cart(request,cart=None):
    try:
        if not cart: cart = Cart(request)
        html=render_to_string('components/base/cart.html',{'cart':cart},request=request)
        data={
            'status' : 'ok',
            'html': html
        }
    except Exception as e:
        data={
            'status':'error',
            'message':e
        }
    return JsonResponse(data, safe=False,json_dumps_params={"ensure_ascii": False})
def api_add_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.loads(request.body)
        try:
            cart.add(Product.objects.get(id=int(data['id'])),int(data['quantity']),data['properties'])
            total_product=len(cart)
            return JsonResponse({'status':'ok','message':'Product added to cart','data':total_product},safe=False,json_dumps_params={"ensure_ascii": False})
        except Exception as e:
            return JsonResponse({'status':'error','message':e},safe=False,json_dumps_params={"ensure_ascii": False})
    return JsonResponse({'status':'error','message':'Could\'t add product to the shopping cart'},safe=False,json_dumps_params={"ensure_ascii": False})
def test(request):
    request.session['currency'] = 'EUR'
    return HttpResponse(Product.get_by_rating())