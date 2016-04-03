from core.tasks.update import update_feeds
from core.models import Feed
from core.signals import get_feed_on_creation
from django.test import TestCase
from django.utils import timezone
from django.db.models.signals import post_save
from unittest.mock import patch
from faker import Factory

fake = Factory.create()


class UpdateTest(TestCase):
    def setUp(self):
        post_save.disconnect(get_feed_on_creation, sender=Feed)

    @patch('core.tasks.fetch.feedparser')
    @patch('core.tasks.fetch.fetch_feed.delay')
    def test_update(self, mock_fetch, mock_feedparser):
        feeds = []
        date = timezone.now().replace(year=1970)
        feeds.append(Feed.objects.create(link=fake.url(),
                                         next_fetch=date))
        for i in range(3):
            date = timezone.now().replace(year=3000)
            feeds.append(Feed.objects.create(link=fake.url(),
                                             next_fetch=date))

        mock_feedparser.parse.side_effect = Exception()
        update_feeds()
        mock_fetch.assert_called_once_with(feeds[0].id)
