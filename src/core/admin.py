from django.contrib import admin
from .tasks.fetch import fetch_feed, fetch_article
from .models import Feed, Article, FeedSubscription, ReadingEntry


class SubscriptionInline(admin.StackedInline):
    model = Feed.subscribers.through
    extra = 0


class ReadingEntryInline(admin.TabularInline):
    model = Article.subscribers.through
    extra = 0


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    actions = ['force_feed_fetch']
    inlines = [SubscriptionInline]
    list_display = ['name', 'link', 'status', 'last_fetch', 'next_fetch',
                    'article_count', 'subscribers_count']
    list_display_links = ['name', 'link']
    list_filter = ['status', 'last_fetch', 'next_fetch']

    def force_feed_fetch(self, request, queryset):
        for feed in queryset:
            fetch_feed.delay(feed.pk)
    force_feed_fetch.short_description = 'Refetch selected feeds'

    def article_count(self, obj):
        return obj.article_set.all().count()

    def subscribers_count(self, obj):
        return obj.subscribers.all().count()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = ['force_article_fetch']
    inlines = [ReadingEntryInline]
    list_display = ['title', 'link', 'status', 'last_fetch',
                    'subscribers_count']
    list_display_links = ['title']
    list_filter = ['status', 'last_fetch']

    def force_article_fetch(self, reuest, queryset):
        for article in queryset:
            fetch_article.delay(article)
    force_article_fetch.description = 'Refetch selected articles'

    def subscribers_count(self, obj):
        return obj.subscribers.all().count()


admin.site.register(FeedSubscription)
admin.site.register(ReadingEntry)
