from django.urls import path
from . import views

app_name = 'kisumu'

urlpatterns = [
    path('index.html', views.index, name='index'),

    path('about.html', views.about, name='about'),

    path('causes_list.html', views.CauseList.as_view(), name='CauseList'),

    path('<slug:slug>/', views.CauseDetail.as_view(), name='CauseDetail'),

    path('blog_list.html', views.blog_list, name='blog_list'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.blog_detail, name='blog_detail'),

    path('tag/<slug:tag_slug>/',
         views.blog_detail, name='blog_detail_by_tag'),

    path('contact.html', views.contact, name='contact'),

    path('search', views.search, name='search'),
]
