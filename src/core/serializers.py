from .models import Feed, Article, ReadingEntry, FeedSubscription
from rest_framework import serializers


class FeedSerializer(serializers.ModelSerializer):
    link = serializers.URLField(max_length=200)

    class Meta:
        model = Feed
        fields = ('link', 'name', 'status', 'last_fetch')
        read_only_fields = ('name', 'status', 'last_fetch')


class ArticleSerializer(serializers.ModelSerializer):
    link = serializers.URLField(max_length=200)

    class Meta:
        model = Article
        fields = ('link', 'title', 'content', 'status', 'last_fetch')
        read_only_fields = ('title', 'content', 'status', 'last_fetch')


class FeedSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    feed = FeedSerializer()

    class Meta:
        model = FeedSubscription
        fields = ('url', 'subscribed_at', 'feed', 'unread')
        read_only_fields = ('subscribed_at',)

    def validate(self, data):
        """Check that user has not already subscribed to the feed"""
        user = self.context['request'].user
        link = data['feed']['link']
        if FeedSubscription.objects.filter(
                user=user, feed__link=link).exists():
            raise serializers.ValidationError(
                'You have already subscribed to this feed')
        return data

    def create(self, validated_data):
        feed_data = validated_data.pop('feed')
        subscription = FeedSubscription(**validated_data)
        feed, _ = Feed.objects.get_or_create(**feed_data)
        subscription.feed = feed
        subscription.save()
        return subscription


class ReadingEntrySerializer(serializers.HyperlinkedModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = ReadingEntry
        fields = ('url', 'article', 'created_at', 'read')
        read_only_fields = ('created_at',)

    def validate(self, data):
        """Check that article is not already in reading list"""
        request = self.context['request']
        link = data['article']['link']
        if request.method == 'POST' and ReadingEntry.objects.filter(
                user=request.user, article__link=link).exists():
            raise serializers.ValidationError(
                'This article is already in your reading list')
        return data

    def create(self, validated_data):
        article_data = validated_data.pop('article')
        entry = ReadingEntry(**validated_data)
        article, _ = Article.objects.get_or_create(**article_data)
        entry.article = article
        entry.save()
        return entry


class ReadingEntryUpdateSerializer(serializers.HyperlinkedModelSerializer):
    article = ArticleSerializer(read_only=True)

    class Meta(ReadingEntrySerializer.Meta):
        pass
