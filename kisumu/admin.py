from django.contrib import admin
from .models import Cause, BlogPost, Comment, Contact


# Register your models here.
@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'cause_image', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'blog_image', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active', 'body')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'message')
