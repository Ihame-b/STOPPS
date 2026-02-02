from django import template
from ecomapp.models import Admin, LinfoxUser

register = template.Library()

@register.filter
def is_admin(user):
    """Check if user is an Admin"""
    if not user or not user.is_authenticated:
        return False
    return Admin.objects.filter(user=user).exists()

@register.filter
def is_linfox_user(user):
    """Check if user is a LinfoxUser"""
    if not user or not user.is_authenticated:
        return False
    return LinfoxUser.objects.filter(user=user).exists()
