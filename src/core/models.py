from django.db import models
from django.contrib.auth.models import User
import core.constants as cst
import uuid


class Feed(models.Model):
    """A feed can be seen as a collection of articles"""
    link = models.URLField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    last_fetch = models.DateTimeField(null=True, blank=True)
    next_fetch = models.DateTimeField(auto_now_add=True)
    subscribers = models.ManyToManyField(User, through='FeedSubscription')
    status = models.IntegerField(choices=cst.Statuses,
                                 default=cst.PENDING_STATUS)

    def __str__(self):
        return self.link


class Article(models.Model):
    """An article represent a web page which content has been saved."""
    link = models.URLField(unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=cst.Statuses,
                                 default=cst.PENDING_STATUS)
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL,
                             blank=True, null=True)
    subscribers = models.ManyToManyField(User, through='ReadingEntry')
    last_fetch = models.DateTimeField(null=True)

    def __str__(self):
        return self.link


class FeedSubscription(models.Model):
    """Association between a user and a feed"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.feed)

    class Meta:
        unique_together = ('user', 'feed')


class ReadingEntry(models.Model):
    """Association between an article and a user"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Reading entry"
        verbose_name_plural = "Reading entries"
        unique_together = ('user', 'article')

    def __str__(self):
        return "{} - {}".format(self.user.username, self.article.link[:50])
