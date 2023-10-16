from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag()
def custom_urlencode(base_url, **kwargs):
    valid_kwargs = {k: v for k, v in kwargs.items() if v and str(v).strip() != ''}
    print(valid_kwargs)
    urlencoded_args = urlencode(valid_kwargs)
    print(urlencoded_args)
    return f'{base_url}?{urlencoded_args}'
    