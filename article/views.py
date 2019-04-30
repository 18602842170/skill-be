import django_filters
import requests
from django.shortcuts import render
from article.models import Article,Comment
from article.filters import ArticleFilter,CommentFilter
from article.serializers import ArticleSerializer,CommentSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.deprecation import MiddlewareMixin
from skill_be.settings import SOCKET_IO_BASEURL
from rest_framework.response import Response
# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (AllowAny,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ArticleFilter
    model_name = 'Article'

    # getbyId查询
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.readCount += 1
        instance.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (AllowAny,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = CommentFilter
    model_name = 'Comment'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response("data is not valid", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        articles = Article.objects.filter(id=request.data.get('article', -1))
        article = None
        if len(articles) != 0:
            article = articles[0]
        instance = serializer.save(article=article)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response("data is not valid", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        articles = Article.objects.filter(id=request.data.get('article', -1))
        article = None
        if len(articles) != 0:
            article = articles[0]
        serializer.save(article=article)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_201_CREATED)
