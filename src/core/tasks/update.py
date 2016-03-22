from celery import shared_task
from django.utils import timezone
from core.models import Feed
from core.tasks.fetch import fetch_feed


@shared_task
def update_feeds():
    """
    Fetch feeds which are due (now > next_fetch)
    """
    feeds = Feed.objects.filter(next_fetch__gte=timezone.now())
    for feed in feeds:
        fetch_feed.delay(feed.id)
