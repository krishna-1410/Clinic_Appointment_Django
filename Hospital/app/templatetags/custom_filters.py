from django import template
from app.models import Payment  # Make sure the model import is correct

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)