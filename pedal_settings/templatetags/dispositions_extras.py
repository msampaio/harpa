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


@register.simple_tag
def dict_get(the_dict, key):
    # Try to fetch from the dict, and if it's not found return an empty string.
    return the_dict.get(key, '')


@register.simple_tag
def get_accident(accidents_string, key, n):
    notes = list('cdefgab')
    accidents = accidents_string.replace(' ', '').replace('(', '').replace(')', '').split(',')
    dic = {}
    for k, v in zip(notes, accidents):
        dic[k] = str(int(v) * n)
    return dic[key]
