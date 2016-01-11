"""leth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from core import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^feeds/$', views.FeedList.as_view()),
    url(r'^feeds/(?P<pk>[0-9]+)/$', views.FeedDetail.as_view()),
    url(r'^articles/$', views.ReadingList.as_view()),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
