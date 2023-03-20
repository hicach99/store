from django.urls import reverse
import requests
import json
from app.models import Product
def currency_converter(request,config,price):
    rates=None
    input=config.currency.code
    try:
        url = f"https://v6.exchangerate-api.com/v6/{config.exchangerate_api}/latest/{input}" if config else 'https://google.com'
        d = requests.get(url).json()
        if config and d["result"] == "success":
            rates=d["conversion_rates"]
    except:
        rates=request.session['rates']
    if input != 'USD':
        ex_target =  rates['USD'] if rates else 1
        result = float(ex_target) * float(price)
    return "%.2f" % result
def create_paypal_order(request,cart,config):
    price=0
    for id,item_id in cart.cart.items():
        price+=float(Product.objects.get(id=id).price)*sum(item['quantity'] for item in item_id)
    response = requests.post(
        url='https://api-m.sandbox.paypal.com/v2/checkout/orders' if config.paypal_sandbox else 'https://api-m.paypal.com/v2/checkout/orders',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.paypal_secret_key}',
        },
        json={
            'intent': 'CAPTURE',
            'application_context': {
                'return_url': 'http://'+request.get_host()+reverse('checkout_process'),
                'cancel_url': 'http://'+request.get_host()+reverse('echec'),
            },
            'purchase_units': [
                {
                'amount': {
                        'currency_code': 'USD',
                        'value': currency_converter(request,config,price),
                    },
                },
            ],
        },
        auth=(config.paypal_public_key, config.paypal_secret_key),
    )
    response_json = json.loads(response.text)
    if 'id' in response_json:
        order_id = response_json['id']
        return order_id, next(link['href'] for link in response.json()['links'] if link['rel'] == 'approve')
    return None, None

def check_paypal_order(order_id,config):
    result=requests.get(
        url=f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}' if config.paypal_sandbox else f'https://api-m.paypal.com/v2/checkout/orders/{order_id}',
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US"
        },
        data={"grant_type":"client_credentials"},
        auth=(config.paypal_public_key, config.paypal_secret_key),
    )
    response=json.loads(result.text)
    return response['id'] if 'id' in response and  response['status'] in ['APPROVED','COMPLETED'] else False
