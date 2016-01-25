from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Feed, Article
from core.tasks.fetch import fetch_feed, fetch_article


@receiver(post_save, sender=Feed)
def get_feed_on_creation(sender, instance, created, **kwargs):
    if created:
        fetch_feed.apply_async((instance.id,), countdown=3)


@receiver(post_save, sender=Article)
def get_article_on_creation(sender, instance, created, **kwargs):
    if created and not instance.content:
        fetch_article.apply_async((instance.id,), countdown=3)
