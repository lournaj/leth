from django.db import models
from django.contrib.auth.models import User


class Feed(models.Model):
    """A feed can be seen as a collection of articles"""
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    next_fetch = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.url)


class Article(models.Model):
    """An article represent a web page which content has been saved."""
    PENDING = 0
    READY = 1
    Statuses = (
        (PENDING, 'Pending'),
        (READY, 'Ready'),
    )
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=Statuses, default=PENDING)
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL,
                             blank=True, null=True)

    def __str__(self):
        return self.url


class FeedSubscription(models.Model):
    """Association between a user and a feed"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user, self.feed)


class ReadingEntry(models.Model):
    """Association between an article and a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Reading entry"
        verbose_name_plural = "Reading entries"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.article.url[:50])
