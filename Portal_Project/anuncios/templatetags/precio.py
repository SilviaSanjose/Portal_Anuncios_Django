from django import template

register = template.Library()


@register.filter(name='precio')
def precio(value):
    return str(value).rstrip('0').rstrip('.')