from django.contrib import admin
from .models import Feed, Article, FeedSubscription, ReadingEntry


admin.site.register(Feed)
admin.site.register(Article)
admin.site.register(FeedSubscription)
admin.site.register(ReadingEntry)
