import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from app.cart import Cart
from app.cmi import create_cmi_order_v1
from app.models import *
from django.template.loader import render_to_string
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from urllib.parse import unquote, urlparse
from app.paypal import check_paypal_order, create_paypal_order
from app.sender import send

# Loading Configuration
try:
    config=Configuration.objects.all()[0]
except:
    config=None

def set_currency(request,code:str):
    request.session['currency']=code.upper()
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
    calculate_rates(request)
    return response
def calculate_rates(request):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{config.exchangerate_api}/latest/{config.currency.code}" if config else 'https://google.com'
        d = requests.get(url).json()
        if config and d["result"] == "success":
            request.session['rates']=d["conversion_rates"]
    except:
        request.session['rates']='hhhhh'
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
    if len(cart)>0:
        return render(
            request,
            'cart.html',
            {
                'config':config,
                'cart':cart,
                'categories':categories,
            }
        )
    return redirect('shop')
def checkout(request):
    cart = Cart(request)
    categories=Category.get_all()
    if len(cart)>0:
        return render(
            request,
            'checkout.html',
            {
                'config':config,
                'cart':cart,
                'categories':categories,
            }
        )
    return redirect('shop')
def remove_cart(request):
    cart = Cart(request)
    product_id=request.GET['id']
    properties=request.GET['properties'].split(',')[0:-1]
    try:
        cart.remove(product_id,[int(p) for p in properties])
    except Exception as e:
        print(e)
    return redirect('cart')
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart')
def update_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.loads(request.body)
        cart.update(data)
    return JsonResponse({'status':'ok'},safe=False,json_dumps_params={"ensure_ascii": False})
def checkout_process(request):
    success=False
    if request.method == 'POST':
        if request.POST.get('payment_method')=='1':
            payment_method='cash on delivery'
            info = {
                'name':request.POST.get('name'),
                'phone':request.POST.get('phone'),
                'email':request.POST.get('email_optional',None),
                'address':request.POST.get('address'),
                'city':request.POST.get('city'),
                'payment_method':payment_method,
            }
            cart = Cart(request)
            order=Order.create_order(info,cart)
            if order: 
                send(order,[],config=config,request=request)
                success=True
    elif request.method == 'GET' and 'info' in request.session:
        if request.session['info']['payment_method']=='cmi':
            cart = Cart(request)
            order=Order.create_order(request.session['info'],cart)
            if order: 
                send(order,[],config=config,request=request)
                del request.session['info']
                success=True
        elif request.session['info']['payment_method']=='paypal' and check_paypal_order(request.session['info']['paypal_order_id'],config):
            cart = Cart(request)
            order=Order.create_order(request.session['info'],cart)
            if order: 
                send(order,[],config=config,request=request)
                del request.session['info']
                success=True
    if success: return redirect('success')
    return redirect('echec')
def success(request):
    categories=Category.get_all()
    cart = Cart(request)
    products=Product.objects.all()
    return render(
        request,
        'success.html',
        {
            'config':config,
            'categories':categories,
            'cart':cart,
            'products':products,
        }
    )
def echec(request):
    categories=Category.get_all()
    cart = Cart(request)
    return render(
        request,
        'echec.html',
        {
            'config':config,
            'categories':categories,
            'cart':cart,
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
def api_create_order(request):
    try:
        if request.method.upper()=='POST':
            url=None
            cart = Cart(request)
            data = json.loads(request.body)
            request.session['info'] = {
                'name':str(data['name']),
                'phone':str(data['phone']),
                'email':str(data['email']),
                'address':str(data['address']),
                'city':str(data['city']),
            }
            if data['payment_method'] == '2':
                cmi_order_id ,url =create_cmi_order_v1(request,cart,config)
                if url:
                    request.session['info']['payment_method']='cmi'
                    request.session['info']['cmi_order_id']=cmi_order_id
            elif data['payment_method'] == '3':
                paypal_order_id ,url = create_paypal_order(request,cart,config)
                if url:
                    request.session['info']['payment_method']='paypal'
                    request.session['info']['paypal_order_id']=paypal_order_id
            if url: return JsonResponse({'status':'ok','url':url}, safe=False)
    except Exception as e:
            return JsonResponse({'status':'error','message':e},safe=False)
    return JsonResponse({'status':'error','message':'Something went wrong'},safe=False)
def test(request):
    return render(
        request,
        'test.html'
    )