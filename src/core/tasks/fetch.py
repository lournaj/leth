from django.utils import timezone
from django.contrib.auth import get_user_model
from celery import shared_task
from core.models import Article, Feed, ReadingEntry, FeedSubscription
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
            article, created = Article.objects.get_or_create(link=post.link)
            if created:
                print("Article created")
            article.title = post.title
            article.content = post.summary
            article.feed = feed
            article.status = cst.READY_STATUS
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
        feed.last_fetch = timezone.now()
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


@shared_task
def import_feed_list(user_id, feed_list):
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    for link in feed_list:
        feed, _ = Feed.objects.get_or_create(link=link)
        FeedSubscription.objects.get_or_create(user=user, feed=feed)
