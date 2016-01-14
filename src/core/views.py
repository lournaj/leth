from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin,
                                   ListModelMixin, DestroyModelMixin)
from .models import ReadingEntry, FeedSubscription
from .serializers import (ReadingEntrySerializer, FeedSubscriptionSerializer)
from .permissions import IsOwner


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
