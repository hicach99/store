from django.template import Library

from app.models import Property
register = Library()

@register.filter
def discount(price, old_price):
    return str(int(100*(1-(price/old_price))))+'%'
@register.filter
def get_property_name(id):
    try:
        return Property.objects.get(id=id).name
    except:
        ''
    

