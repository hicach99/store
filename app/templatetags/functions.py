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
def convert(amount:float,output)-> str:
    input=config.currency.code if config else 'MAD'
    symbol=Currency.objects.get(code=output).symbol
    result=amount
    print(input,output)
    if input != output:
    # Converter
        url = f"https://open.er-api.com/v6/latest/{input}"
        d = requests.get(url).json()
        if config and d["result"] == "success":
            ex_target =  d["rates"][output]
            result = float(ex_target) * float(amount)
    if len(symbol)>=2:
        result = "%.2f " % result+symbol
    else:
        result = symbol+"%.2f" % result
    return result