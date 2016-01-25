from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class FeedTest(APITestCase):
    def test_not_authenticated_user(self):
        url = reverse('feedsubscription-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
