from django.contrib import admin
from .tasks import fetch_feed
from .models import Feed, Article, FeedSubscription, ReadingEntry


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    actions = ['force_feed_fetch']

    def force_feed_fetch(self, request, queryset):
        for feed in queryset:
            fetch_feed.delay(feed.pk)
    force_feed_fetch.short_description = "Refetch selected feeds"


admin.site.register(Article)
admin.site.register(FeedSubscription)
admin.site.register(ReadingEntry)
