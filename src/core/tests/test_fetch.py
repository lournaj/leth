from core.tasks.fetch import retrieve_feed_content, retrieve_article_content
from core.models import Feed, Article
import core.constants as cst
from django.test import TestCase
from unittest.mock import patch
from faker import Factory

fake = Factory.create()


class FakeArticle:
    def __init__(self):
        self.link = fake.url()
        self.title = fake.catch_phrase()
        self.summary = fake.text()


class FakeFeed:
    def __init__(self, count=1):
        self.entries = [FakeArticle() for i in range(count)]


class FeedFetchTest(TestCase):
    @patch('core.tasks.fetch.feedparser')
    def test_fetch_error(self, mock_feedparser):
        feed = Feed(link="http://test.test/test.xml")
        mock_feedparser.parse.side_effect = Exception()
        retrieve_feed_content(feed)
        mock_feedparser.parse.assert_called_with(feed.link)
        self.assertEqual(feed.status, cst.ERROR_STATUS)

    @patch('core.tasks.fetch.feedparser')
    def test_fetch(self, mock_feedparser):
        feed = Feed(link='http//test.test/test.xml')
        fake_feed = FakeFeed()
        mock_feedparser.parse.return_value = fake_feed
        retrieve_feed_content(feed)
        mock_feedparser.parse.assert_called_with(feed.link)
        article = Article.objects.get(link=fake_feed.entries[0].link)
        self.assertEqual(article.status, cst.READY_STATUS)
        self.assertEqual(article.title, fake_feed.entries[0].title)


class ArticleFetchTest(TestCase):
    @patch('core.tasks.fetch.requests')
    def test_fetch_error(self, mock_requests):
        article = Article(link='http://test.test/test.html')
        mock_requests.get.side_effect = Exception()
        retrieve_article_content(article)
        mock_requests.get.assert_called_with(article.link)
        self.assertEqual(article.status, cst.ERROR_STATUS)
