from .models import Feed, Article
from rest_framework import serializers


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('url', 'name')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ('url', 'title', 'content', 'status', 'feed')
