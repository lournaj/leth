from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Feed
from core.tasks import fetch_feed

@receiver(post_save, sender=Feed)
def get_feed_on_creation(sender, instance, created, **kwargs):
    if created:
        fetch_feed.delay(instance.id)
