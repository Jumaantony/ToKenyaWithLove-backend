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


@register.inclusion_tag('recent_posts.html')
def recent_posts(count=3):
    most_recent_post = BlogPost.published.order_by('-publish')[:count]
    return {'most_recent_post': most_recent_post}


@register.inclusion_tag('most_popular_causes.html')
def recent_cause(count=3):
    most_recent_cause = Cause.objects.filter(status='publish').order_by('-publish')[:count]
    return {'most_recent_cause': most_recent_cause}


@register.simple_tag
def get_most_commented_posts(count=3):
    return BlogPost.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
