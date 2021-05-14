from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Cause, BlogPost


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


class CauseList(ListView):
    queryset = Cause.objects.filter(status='publish').order_by \
        ('-publish')
    template_name = 'causes_list.html'
    paginate_by = 4


class CauseDetail(DetailView):
    model = Cause
    template_name = 'causes_detail.html'


def blog_list(request):
    posts = BlogPost.published.all()

    return render(request,
                  'blog_list.html',
                  {'posts': posts})


def blog_detail(request, year, month, day, post):
    post = get_object_or_404(BlogPost,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog_detail.html',
                  {'post': post})


def contact(request):
    return render(request, 'contact.html', {})
