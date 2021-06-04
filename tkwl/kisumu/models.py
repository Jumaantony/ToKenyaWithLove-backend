from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


class Cause(models.Model):
    STATUS_CHOICES = (
        ('draft', "Draft"),
        ('publish', "Publish"),
    )

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    cause_image = models.ImageField(upload_to='CauseImage/')
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', "Draft"),
        ('published', "Published"),
    )

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    blog_image = models.ImageField(upload_to='BlogImage/')
    body = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')
    tags = TaggableManager()

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('kisumu:blog_detail', args=[self.publish.year,
                                                   self.publish.month,
                                                   self.publish.day,
                                                   self.slug])


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=20)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.blogpost}'
