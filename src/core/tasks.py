from django.utils import timezone
from celery import shared_task
from .models import Article, Feed, ReadingEntry
import core.constants as cst
import feedparser
import requests
from readability.readability import Document


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
            for subscriber in feed.subscribers.all():
                entry = ReadingEntry(user=subscriber, article=article)
                entry.save()
    except Exception as e:
        print(e)
        feed.status = cst.ERROR_STATUS
        feed.last_fetch = timezone.now()
        feed.save()
    else:
        if feed.status != cst.READY_STATUS:
            feed.status = cst.READY_STATUS
        if not feed.name:
            feed.name = data.feed.title
        feed.save()


@shared_task
def fetch_article(article_id):
    article = Article.objects.get(pk=article_id)
    try:
        response = requests.get(article.link)
        if response.ok:
            doc = Document(response.content)
            article.content = doc.summary()
            article.title = doc.title()
            article.status = cst.READY_STATUS
        else:
            article.status = cst.ERROR_STATUS
        article.last_fetch = timezone.now()
        article.save()
    except Exception as e:
        print(e)
        article.status = cst.ERROR_STATUS
        article.last_fetch = timezone.now()
        article.save()
