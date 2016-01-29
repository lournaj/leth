from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from core.models import Feed, FeedSubscription
from rest_framework.test import APITestCase
from rest_framework import status
from lxml import etree
from datetime import datetime
from django.utils import timezone


class FeedTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_feed', 'feed@localhost')
        self.url = reverse('feedsubscription-list')

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_feed_creation(self):
        link = 'http://test.nowhere/feed.atom'
        data = {'feed': {'link': link}}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset({'link': link}, response.data['feed'])
        self.assertEqual(Feed.objects.get().link, link)

    def test_duplicate_feed_error(self):
        data = {'feed': {'link': 'http://test.nowhere/feed.atom'}}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'non_field_errors': ['You have already subscribed to this feed']}
        )

    def test_feed_list(self):
        feed = Feed.objects.create(link='http://test.nowhere/feed.atom')
        FeedSubscription.objects.create(feed=feed, user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)


class ArticleTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_article',
                                             'article@localhost')
        self.url = reverse('readingentry-list')

    def test_duplicate_article_error(self):
        data = {'article': {'link': 'http://test.nowhere/test.html'}}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'non_field_errors':
             ['This article is already in your reading list']}
        )

    def test_article_read(self):
        data = {'article': {'link': 'http://test.nowhere/test.html'}}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        reading_date = '2016-01-01T12:12:12Z'
        data['read'] = reading_date
        response = self.client.put(data['url'], data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['read'], reading_date)


class OPMLTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_opml',
                                             'opml@localhost')
        self.url = reverse('opml-list')

    def test_opml_export(self):
        self.client.force_authenticate(user=self.user)
        data = {'feed': {'link': 'https://somefeed.local/feed.rss'}}
        response = self.client.post(reverse('feedsubscription-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {'feed': {'link': 'https://somefeed.local/feed.atom'}}
        response = self.client.post(reverse('feedsubscription-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        opml = etree.fromstring(response.content)
        self.assertEqual(len(opml[1]), 2)
        dt = datetime.strptime(opml[0][0].text, '%a, %d %b %Y %H:%M:%S %z')
        self.assertEqual(dt.date(), timezone.now().date())
