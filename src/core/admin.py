from django.contrib import admin
from .models import Feed, Article


class FeedAdmin(admin.ModelAdmin):
    model = Feed


class ArticleAdmin(admin.ModelAdmin):
    model = Article

admin.site.register(Feed, FeedAdmin)
admin.site.register(Article, ArticleAdmin)
