from rest_framework import generics
from .models import ReadingEntry, FeedSubscription
from .serializers import (ReadingEntrySerializer, FeedSubscriptionSerializer)


class ReadingList(generics.ListCreateAPIView):
    serializer_class = ReadingEntrySerializer

    def get_queryset(self):
        user = self.request.user
        return ReadingEntry.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReadingEntrySerializer

    def get_queryset(self):
        user = self.request.user
        return ReadingEntry.objects.filter(user=user)


class FeedList(generics.ListCreateAPIView):
    serializer_class = FeedSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return FeedSubscription.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FeedDetail(generics.RetrieveDestroyAPIView):
    serializer_class = FeedSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return FeedSubscription.objects.filter(user=user)
