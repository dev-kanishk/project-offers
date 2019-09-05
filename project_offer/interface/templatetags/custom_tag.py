from django import template
register = template.Library()
from ..models import Categories

@register.simple_tag
def get_all_categories():
    return Categories.objects.all()