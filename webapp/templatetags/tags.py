#ARCHIVO PARA EL REGISTRO DE NUEVOS TAGS, ESTOS SE USAN EN LAS PLANTILLAS HTML
from django import template
from django.contrib.auth.models import Group 
from webapp.models import *

register = template.Library()
@register.filter(name='has_group') 
def has_group(user, group_name):
    group = Group.objects.get(name=group_name) 
    return user.groups.filter(name=group_name).exists()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price