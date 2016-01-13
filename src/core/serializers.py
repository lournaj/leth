from .models import Feed, Article, ReadingEntry, FeedSubscription
from rest_framework import serializers


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('link', 'name', 'status')
        read_only_fields = ('name', 'status', 'link')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('link', 'title', 'content', 'status')
        read_only_fields = ('title', 'content', 'status', 'link')


class FeedSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    feed = FeedSerializer()

    class Meta:
        model = FeedSubscription
        fields = ('url', 'subscribed_at', 'feed')
        read_only_fields = ('subscribed_at',)

    def create(self, validated_data):
        feed_data = validated_data.pop('feed')
        subscription = FeedSubscription(**validated_data)
        try:
            feed = Feed.objects.get(link=feed_data.get('link'))
        except Feed.DoesNotExist:
            feed = Feed.objects.create(**feed_data)
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
        try:
            article = Article.objects.get(link=article_data.get('link'))
        except Article.DoesNotExist:
            article = Feed.objects.create(**article_data)
        entry.article = article
        entry.save()
        return entry
