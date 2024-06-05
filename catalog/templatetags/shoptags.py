from django import template
from django.utils.http import urlencode
from catalog.models import Category, Item




register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)




@register.simple_tag(name='all_categories')
def get_categories():
    return Category.objects.all()




@register.simple_tag(name='get_the_most_liked_items')
def get_the_most_liked_items(user=None):
    return Item.objects.filter(active=True).exclude(seller=user).order_by("-likes")[:4]