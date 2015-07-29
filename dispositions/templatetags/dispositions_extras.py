from django import template

register = template.Library()


@register.filter(name='radial_format')
def radial_format(value):
    left = int(value / 10000)
    right = value % 10000
    return '{:03} {:04}'.format(left, right)


@register.filter(name='scalar_format')
def scalar_format(value):
    left = int(value / 10000)
    right = value % 10000
    return '{:03}{:04}'.format(left, right)
