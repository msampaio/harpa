from django import template

register = template.Library()

@register.filter(name='spaced_format')
def spaced_format(value):
    left = int(value / 10000)
    right = value % 10000
    return '{:03} {:04}'.format(left, right)
