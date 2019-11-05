from django import template
import pycountry


register = template.Library()


@register.filter(name='get_country_name')
def get_country_name(value):
    return pycountry.countries.lookup(value).name
