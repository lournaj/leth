from rest_framework import filters
from django_filters import (NumberFilter, DateTimeFromToRangeFilter,
                            NumericRangeFilter)
from core.models import ReadingEntry, FeedSubscription


class ReadingEntryFilter(filters.FilterSet):
    read = DateTimeFromToRangeFilter()
    created_at = DateTimeFromToRangeFilter()
    feed = NumberFilter(name='article__feed')

    class Meta:
        model = ReadingEntry
        fields = ['read', 'created_at', 'feed']


class FeedSubscriptionFilter(filters.FilterSet):
    subscribed_at = DateTimeFromToRangeFilter()

    class Meta:
        model = FeedSubscription
        fields = ['subscribed_at']
