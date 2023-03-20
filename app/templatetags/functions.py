from django.template import Library
import requests
from app.models import Configuration, Property,Currency
register = Library()

try:
    config=Configuration.objects.all()[0]
except:
    config=None

@register.filter
def discount(price, old_price):
    return str(int(100*(1-(price/old_price))))+'%'
@register.filter
def get_property_name(id):
    try:
        return Property.objects.get(id=id).name
    except:
        ''
@register.filter
def capitalize(string:str):
    return string[0].upper()+string[1:].lower()

@register.filter
def filterby(l,filter:str):
    new=[]
    for i in l:
        if i.type.name==filter: new.append(i)
    return new

@register.filter
def convert(amount:float,request)-> str:
    output=request.session['currency']
    rates=request.session['rates']
    input=config.currency.code
    symbol=Currency.objects.get(code=output).symbol
    result=amount
    if input != output:
        ex_target =  rates[output] if rates else 1
        result = float(ex_target) * float(amount)
    if len(symbol)>=2:
        result = "%.2f " % result+symbol
    else:
        result = symbol+"%.2f" % result
    return result

@register.filter
def instagram_feed(n):
    instagram_access_token = '2406057572895918|ENcC-8n8F4ntLZw4Lgpj5g3RVMc'
    api_url = f'https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url&access_token={instagram_access_token}&limit=10'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()['data']
        return [post['media_url'] for post in data]
    return  response.content