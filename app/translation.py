from modeltranslation.translator import TranslationOptions,register
from app.models import *

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )
@register(PropertyType)
class PropertyTypeTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )
@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )
@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'status',
        'description',
        'product_details',
    )
@register(ProductInformation)
class ProductInformationTranslationOptions(TranslationOptions):
    fields = (
        'key',
        'value',
    )
