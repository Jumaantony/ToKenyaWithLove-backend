from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Cause, BlogPost
from django.core.paginator import *
from .forms import CommentForm
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchHeadline, SearchQuery
from django.core.mail import send_mail
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


class CauseList(ListView):
    queryset = Cause.objects.filter(status='publish').order_by('-publish')
    template_name = 'causes_list.html'
    paginate_by = 4


class CauseDetail(DetailView):
    model = Cause
    template_name = 'causes_detail.html'


def blog_list(request, ):
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


def blog_detail(request, year, month, day, post, tag_slug=None):
    post = get_object_or_404(BlogPost,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # adding Tags in Posts
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])

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

    # list of similar functions
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = BlogPost.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   'tag': tag,
                   })


def contact(request):
    if request.method == 'POST':
        sender_name = request.POST['sender_name']
        sender_email = request.POST['sender_email']
        message = request.POST['message']

        # send an email
        send_mail(
            sender_name,  # subject
            message,  # message
            sender_email,  # from email
            ['odongoanton2@gmail.com'],  # To Email
        )

        context = {
            'sender_name': sender_name,
            'sender_email': sender_email,
            'message': message
        }

        return render(request, 'contact.html', context)
    else:
        return render(request, 'contact.html', {})


def search(request):
    if request.method == 'GET':
        query = request.GET['search_query']
        search_results = BlogPost.objects.annotate(
            search=SearchVector('title', 'body'),
        ).filter(search=query)

        context = {'search_results': search_results,
                   'query': query}
        return render(request, 'search.html', context)


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


# subscription Logic
def subscribe(email):
    """"
    Contains code handling the communication to the
    mailchimp to create a contact/member in an audience list
    """
    mailchimp = Client
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed"
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occured: {}".format(error.text))


def subscription(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)

        messages.success(request, "Email received. thank You! ")

    return render(request, 'subscribe.html')
