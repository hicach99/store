from django import forms
from django.forms.models import inlineformset_factory
from .models import *
from django.forms.widgets import FileInput

class ImageWidget(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        html += value.img_preview()
        return html

try:
    config=Configuration.objects.all()[0]
except:
    config=None

class OrderItemInlineFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = OrderItem.objects.none()
class ImageInlineFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Image.objects.none()
class InformationInlineFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = ProductInformation.objects.none()

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=('product','properties','quantity','total_price'),
    extra=1,
    formset=OrderItemInlineFormset,
    widgets={
        'product': ImageWidget(),
        'total_price':forms.FloatField(help_text=config.currency if config else "MAD")
    },
    
)

ImageFormSet = inlineformset_factory(Product, Image, fields=('image',), extra=3, formset=ImageInlineFormset)
InformationFormSet = inlineformset_factory(Product, ProductInformation, fields=('key','value',), extra=1, formset=InformationInlineFormset)

class PropertyAdminForm(forms.ModelForm):
    value=forms.CharField(required=False,help_text="For Colors Enter a HEX value Ex: #fff or #ffffff for white \nElse leave it blank")
    class Meta:
        model = Property
        fields = '__all__'
class ProductAdminForm(forms.ModelForm):
    price=forms.FloatField(help_text=config.currency if config else "MAD")
    old_price=forms.FloatField(help_text=config.currency if config else "MAD")
    images = ImageFormSet()
    informations = InformationFormSet()
    tags = forms.ModelMultipleChoiceField(required=False,queryset=Tag.objects.all())
    properties = forms.ModelMultipleChoiceField(required=False,queryset=Property.objects.all())
    class Meta:
        model = Product
        fields = '__all__'

class OrderAdminForm(forms.ModelForm):
    total_price=forms.FloatField(help_text=config.currency if config else "MAD")
    items = OrderItemFormSet()
    class Meta:
        model = Product
        fields = '__all__'

class ConfigurationAdminForm(forms.ModelForm):
    keywords=forms.CharField(help_text='Enter keywords separated by (,) Ex: apple,windows,amazon')
    email_recivers=forms.CharField(required=False,help_text='Enter emails separated by (,) Ex: example1@ex.com,example2@ex.com,example3@ex.com', widget=forms.Textarea(attrs={'placeholder': 'example1@ex.com , example2@ex.com , example3@ex.com'}))
    telegram_recivers=forms.CharField(required=False,help_text='Enter telegram IDs separated by (,) Ex: 012345,54758,4557557', widget=forms.TextInput(attrs={'placeholder': '012345 , 54758 , 4557557'}))
    class Meta:
        model = Configuration
        fields = '__all__'