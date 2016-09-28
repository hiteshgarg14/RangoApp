from django import template
from Rango.models import Category

"""
Remember to Restart the Server!
If the server does not restart, they wont be registered by
Django, and you will get confused and irritated.
"""
register = template.Library()

@register.inclusion_tag('Rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'act_cat': cat}
