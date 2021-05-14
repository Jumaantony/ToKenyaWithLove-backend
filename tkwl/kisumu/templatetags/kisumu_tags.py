from django import template
from ..models import BlogPost, Cause
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = BlogPost.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('popular_causes.html')
def show_popular_causes(count=5):
    popular_causes = Cause.objects.filter(status='publish').order_by('-publish')[:count]
    return {'popular_causes': popular_causes}
