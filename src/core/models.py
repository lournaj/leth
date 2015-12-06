from django.db import models


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

    def __str__(self):
        return self.url
