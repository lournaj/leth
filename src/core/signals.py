from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Feed, Article
from core.tasks import fetch_feed, fetch_article


@receiver(post_save, sender=Feed)
def get_feed_on_creation(sender, instance, created, **kwargs):
    if created:
        fetch_feed.delay(instance.id)


@receiver(post_save, sender=Article)
def get_article_on_creation(sender, instance, created, **kwargs):
    if created and not instance.content:
        fetch_article.delay(instance.id)
