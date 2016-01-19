from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from core.models import ReadingEntry, Article
from core.permissions import IsOwner


class PermissionsTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create(username='owner', email='owner@local')
        self.other = User.objects.create(username='other', email='other@local')
        article = Article.objects.create(link='http://nowhere.local')
        self.entry = ReadingEntry.objects.create(user=self.owner,
                                                 article=article)
        self.factory = RequestFactory()

    def test_owner_user(self):
        request = self.factory.get('/whatever/')
        request.user = self.owner
        perm = IsOwner()
        self.assertTrue(perm.has_object_permission(request, None, self.entry))
        request.user = self.other
        self.assertFalse(perm.has_object_permission(request, None, self.entry))
