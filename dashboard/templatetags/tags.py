import re
from django.core.urlresolvers import reverse, NoReverseMatch
from django import template

register = template.Library()

@register.simple_tag
def active(request, view_name):
    try:
        pattern = reverse(view_name)
        #if re.match(pattern, request.path):
        if pattern == request.path:
            return 'active'
    except NoReverseMatch:
        return ''
