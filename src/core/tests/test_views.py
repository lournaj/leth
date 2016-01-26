from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from core.models import Feed
from rest_framework.test import APITestCase
from rest_framework import status


class FeedTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'noone@nowhere.com')

    def test_not_authenticated_user(self):
        url = reverse('feedsubscription-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_feed_creation(self):
        url = reverse('feedsubscription-list')
        link = 'http://www.test.net/feed.atom'
        data = {'feed': {'link': link}}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset({'link': link}, response.data['feed'])
        self.assertEqual(Feed.objects.get().link, link)

    def test_duplicate_feed_error(self):
        url = reverse('feedsubscription-list')
        data = {'feed': {'link': 'http://www.test.net/feed.atom'}}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'non_field_errors': ['You have already subscribed to this feed']}
        )
