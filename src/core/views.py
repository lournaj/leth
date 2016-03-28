from rest_framework import permissions, status, filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin,
                                   ListModelMixin, DestroyModelMixin,
                                   UpdateModelMixin)
from .models import ReadingEntry, FeedSubscription
from .serializers import (ReadingEntrySerializer, FeedSubscriptionSerializer,
                          ReadingEntryUpdateSerializer)
from .permissions import IsOwner
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from lxml import etree
from .tasks.fetch import import_feed_list
from .filters import ReadingEntryFilter, FeedSubscriptionFilter


class FeedViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    serializer_class = FeedSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = ('subscribed_at',)
    filter_class = FeedSubscriptionFilter

    def get_queryset(self):
        user = self.request.user
        return FeedSubscription.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OPMLViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """Import/export OPML files"""

    def list(self, request, *args, **kwargs):
        """Export user feed in OPML"""
        feeds = request.user.feed_set.all()
        response = HttpResponse(content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="leth_opml.xml"'
        t = loader.get_template('core/opml.xml')
        c = {'feeds': feeds, 'date': timezone.now()}
        response.write(t.render(c))
        return response

    def create(self, request, *args, **kwargs):
        """Import OPML file"""
        if request.FILES:
            try:
                f = request.FILES['file']
                feeds = []
                for link in etree.parse(f).xpath('//@xmlUrl'):
                    feeds.append(link)
                import_feed_list.delay(request.user.id, feeds)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception:
                return Response('OPML parsing failed',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('No file uploaded',
                            status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(CreateModelMixin,
                     RetrieveModelMixin,
                     ListModelMixin,
                     DestroyModelMixin,
                     UpdateModelMixin,
                     GenericViewSet):
    serializer_class = ReadingEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = ('read', 'created_at')
    filter_class = ReadingEntryFilter

    def get_serializer_class(self):
        if self.action == 'update':
            return ReadingEntryUpdateSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        return ReadingEntry.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
