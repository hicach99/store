import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.cart import Cart
from app.models import *
from django.template.loader import render_to_string
# Loading Configuration
try:
    config=Configuration.objects.all()[0]
except:
    config=None
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
    products=None
    if 'category' in request.GET:
        products=Product.get_by_category(slug=request.GET['category'])
    elif 'tag' in request.GET:
        products=Product.get_by_tag(slug=request.GET['tag'])
    elif 'q' in request.GET:
        pass
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
            cart.add(Product.objects.get(id=data['id']),data['quantity'],data['properties'])
            total_product=len(cart)
            return JsonResponse({'status':'ok','message':'Product added to cart','data':total_product},safe=False,json_dumps_params={"ensure_ascii": False})
        except Exception as e:
            return JsonResponse({'status':'error','message':e},safe=False,json_dumps_params={"ensure_ascii": False})
    return JsonResponse({'status':'error','message':'Could\'t add product to the shopping cart'},safe=False,json_dumps_params={"ensure_ascii": False})
def test(request):
    return HttpResponse(Product.get_by_rating())