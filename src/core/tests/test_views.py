from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from core.models import Feed, FeedSubscription
from rest_framework.test import APITestCase
from rest_framework import status


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
            {'non_field_errors': ['This article is already in your reading list']}
        )
