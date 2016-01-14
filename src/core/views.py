from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin,
                                   ListModelMixin, DestroyModelMixin)
from .models import ReadingEntry, FeedSubscription
from .serializers import (ReadingEntrySerializer, FeedSubscriptionSerializer)
from .permissions import IsOwner


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'feeds': reverse('feedsubscription-list', request=request,
                         format=format),
        'articles': reverse('readingentry-list', request=request,
                            format=format),
    })


class FeedViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    serializer_class = FeedSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return FeedSubscription.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleViewSet(CreateModelMixin,
                     RetrieveModelMixin,
                     ListModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):
    serializer_class = ReadingEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return ReadingEntry.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
