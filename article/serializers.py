from rest_framework import serializers

from skill_be.utils.myclass import DynamicFieldsModelSerializer
from article.models import Article,Comment


class ArticleSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        depth = 1


class CommentSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1
