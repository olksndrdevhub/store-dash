from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag()
def custom_urlencode(base_url, **kwargs):
    try:
        valid_kwargs = {k: v for k, v in kwargs.items() if v and str(v).strip() != '' and not (k == 'page' and v == 1 or v == '1')}
        urlencoded_args = urlencode(valid_kwargs)
        return f'{base_url}?{urlencoded_args}'
    except Exception as e:
        print(e)
        return base_url
    