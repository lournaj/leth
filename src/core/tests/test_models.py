from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Feed, Article, ReadingEntry, FeedSubscription


class StrTest(TestCase):

    def test_feed_str(self):
        link = 'http://somewhere.com/feed.rss'
        feed = Feed(link=link)
        self.assertEqual(str(feed), link)

    def test_article_str(self):
        link = 'http://somenews.fr/article.html'
        article = Article(link=link)
        self.assertEqual(str(article), link)

    def test_reading_entry_str(self):
        username = 'test'
        link = 'https://www.superlink.com/article.html'
        article = Article(link=link)
        user = User(username=username)
        entry = ReadingEntry(user=user, article=article)
        self.assertEqual("{} - {}".format(username, link[:50]), str(entry))

    def test_subscription_str(self):
        username = 'test'
        link = 'https://www.somewhere.com/feed.atom'
        user = User(username=username)
        feed = Feed(link=link)
        subscription = FeedSubscription(user=user, feed=feed)
        self.assertEqual("{} - {}".format(username, link), str(subscription))
