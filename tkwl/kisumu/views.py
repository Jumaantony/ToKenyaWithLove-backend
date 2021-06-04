from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Cause, BlogPost
from django.core.paginator import *
from .forms import CommentForm


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
    p = Paginator(posts, 3)  # paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return the last page
        page_obj = p.page(p.num_pages)

    context = {'posts': page_obj}
    return render(request,
                  'blog_list.html',
                  context)


def blog_detail(request, year, month, day, post):
    post = get_object_or_404(BlogPost,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # list of active comments
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # comment posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create a new comment but do not save in the database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm

    return render(request,
                  'blog_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   })


def contact(request):
    return render(request, 'contact.html', {})
