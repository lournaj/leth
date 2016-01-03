from rest_framework import viewsets
from .models import Feed, Article
from .serializers import FeedSerializer, ArticleSerializer


class FeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint for feeds
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
