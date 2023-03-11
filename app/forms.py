from django import forms
from django.forms.models import inlineformset_factory
from .models import *

class ImageInlineFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Image.objects.none()
class InformationInlineFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = ProductInformation.objects.none()

ImageFormSet = inlineformset_factory(Product, Image, fields=('image',), extra=3, formset=ImageInlineFormset)
InformationFormSet = inlineformset_factory(Product, ProductInformation, fields=('key','value',), extra=1, formset=InformationInlineFormset)

class PropertyAdminForm(forms.ModelForm):
    value=forms.CharField(required=False,help_text="For Colors Enter a HEX value Ex: #fff or #ffffff for white \nElse leave it blank")
    class Meta:
        model = Property
        fields = '__all__'
class ProductAdminForm(forms.ModelForm):
    price=forms.FloatField(help_text="USD")
    old_price=forms.FloatField(help_text="USD")
    images = ImageFormSet()
    informations = InformationFormSet()
    tags = forms.ModelMultipleChoiceField(required=False,queryset=Tag.objects.all())
    properties = forms.ModelMultipleChoiceField(required=False,queryset=Property.objects.all())
    class Meta:
        model = Product
        fields = '__all__'