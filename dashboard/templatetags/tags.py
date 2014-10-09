import re
from django.core import urlresolvers
from django import template

register = template.Library()

@register.simple_tag
def active(request, view_name):
    try:
        pattern = urlresolvers.reverse(view_name)
        #if re.match(pattern, request.path):
        if pattern == request.path:
            return 'active'
    except urlresolvers.NoReverseMatch:
        return ''
