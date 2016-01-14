from .models import Feed, Article, ReadingEntry, FeedSubscription
from rest_framework import serializers


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('link', 'name', 'status', 'last_fetch', 'next_fetch')
        read_only_fields = ('name', 'status', 'last_fetch', 'next_fetch')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('link', 'title', 'content', 'status', 'last_fetch')
        read_only_fields = ('title', 'content', 'status', 'last_fetch')


class FeedSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    feed = FeedSerializer()

    class Meta:
        model = FeedSubscription
        fields = ('url', 'subscribed_at', 'feed')
        read_only_fields = ('subscribed_at',)

    def create(self, validated_data):
        feed_data = validated_data.pop('feed')
        subscription = FeedSubscription(**validated_data)
        feed = Feed.objects.get_or_create(**feed_data)
        subscription.feed = feed
        subscription.save()
        return subscription


class ReadingEntrySerializer(serializers.HyperlinkedModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = ReadingEntry
        fields = ('url', 'article', 'created_at', 'read')
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        article_data = validated_data.pop('article')
        entry = ReadingEntry(**validated_data)
        article = Article.objects.get_or_create(**article_data)
        entry.article = article
        entry.save()
        return entry
