from django import template
from network.models import *

register = template.Library()

@register.filter
def is_liked_by(post, user):
    return post.likes.filter(pk=user.id).exists()