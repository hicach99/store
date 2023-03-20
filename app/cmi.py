
from django.urls import reverse
import requests
from app.models import Order, Product
import hashlib


def create_cmi_order(request,cart,config):
    price=0
    for id,item_id in cart.cart.items():
        price+=float(Product.objects.get(id=id).price)*sum(item['quantity'] for item in item_id)
    cmi_url = 'https://test.cmi.co.ma/payment/rest/register.do' if config.cmi_sandbox else 'https://www.cmi.co.ma/payment/rest/register.do'
    order_id = str(str(int(Order.objects.last().id)+1)) if Order.objects.last() else '1'
    return_url = 'http://'+request.get_host()+reverse('checkout_process')
    signature = hashlib.sha256(f'{price}:{config.currency}:{order_id}:{return_url}:{config.cmi_merchant_id}:{config.cmi_secret_key}'.encode('utf-8')).hexdigest()
    response = requests.post(
        cmi_url,
        data={
            'price': price,
            'currency': config.currency,
            'orderNumber': order_id,
            'returnUrl': return_url,
            'failUrl': 'http://'+request.get_host()+reverse('echec'),
            'merchantId': config.cmi_merchant_id,
            'language': 'fr',
            'jsonParams': '{}',
            'signature':signature,
        },
    )
    if response.status_code == 200:
        return order_id,response.json().get('formUrl'), signature
    request.session['log']=response.content.decode()
    return None, None, None
def create_cmi_order_v1(request,cart,config):
    price=0
    for id,item_id in cart.cart.items():
        price+=float(Product.objects.get(id=id).price)*sum(item['quantity'] for item in item_id)
    # Set up the required parameters for the payment request
    params = {
        'version': 'V1',
        'amount': price,
        'currency': config.currency,
        'language': 'fr',
        'merchant_id': config.cmi_merchant_id,
        'terminal_id': config.cmi_secret_key,
        'order_id': str(str(int(Order.objects.last().id)+1)) if Order.objects.last() else '1',
        'description': 'your_transaction_description',
        'return_url': 'http://'+request.get_host()+reverse('checkout_process'),
        'cancel_url': 'http://'+request.get_host()+reverse('echec'),
        'notify_url': 'http://'+request.get_host()+reverse('echec'),
    }

    # Send a request to the CMI payment gateway API to create the transaction
    response = requests.post('https://testpayment.cmi.co.ma/payment/rest/register.do', data=params)

    # Handle the response from the CMI payment gateway API
    if response.status_code == 200:
        # Parse the response to extract the transaction ID and redirect the user to the payment page
        response_data = response.json()
        return response_data['orderId'], response_data['formUrl']
    request.session['log']=response.content.decode()
    return None, None
def check_cmi_order(request,config):
    amount = request.GET.get('amount')
    currency = request.GET.get('currency')
    order_id = request.GET.get('orderNumber')
    payment_status = request.GET.get('status')
    expected_signature = hashlib.sha256(f'{amount}:{currency}:{order_id}:{payment_status}:{config.cmi_secret_key}'.encode('utf-8')).hexdigest()
    if request.session['info']['signiture'] != expected_signature:
        return False
    return True