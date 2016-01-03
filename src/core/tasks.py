from celery import shared_task
from .models import Article, Feed
import feedparser


@shared_task
def fetch_feed(feed_id):
    try:
        feed = Feed.objects.get(pk=feed_id)
        data = feedparser.parse(feed.url)
        for post in data['items']:
            print(post)
            article = Article(url=post['link'], title=post['title'], content=post['description'], feed=feed)
            article.save()
    except Exception as e:
        print(e)
        pass
