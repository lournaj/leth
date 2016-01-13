from django.utils import timezone
from celery import shared_task
from .models import Article, Feed
import core.constants as cst
import feedparser


@shared_task
def fetch_feed(feed_id):
    feed = Feed.objects.get(pk=feed_id)
    try:
        data = feedparser.parse(feed.link)
        for post in data.entries:
            article = Article(link=post.link, title=post.title,
                              content=post.summary, feed=feed,
                              status=cst.READY_STATUS)
            article.save()
    except Exception as e:
        print(e)
        feed.status = cst.ERROR_STATUS
        feed.save()
    else:
        if feed.status != cst.READY_STATUS:
            feed.status = cst.READY_STATUS
        if not feed.name:
            feed.name = data.feed.title
        feed.last_fetch = timezone.now()
        feed.save()
