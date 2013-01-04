from django import template

register = template.Library()

@register.filter
def percentage(decimal):
    return '{0:.0%}'.format(float(decimal))
