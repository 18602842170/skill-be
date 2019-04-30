import django_filters
from django.db.models import Q
from article.models import Article,Comment


class ArticleFilter(django_filters.rest_framework.FilterSet):

    search = django_filters.rest_framework.CharFilter(
        method='search_func')

    # 标题，简介，标签的联合like查询，不区分大小写
    def search_func(self, queryset, name, value):
        return queryset.filter(Q(label__icontains=value) | Q(title__icontains=value) | Q(outline__icontains=value))


    order_by =  django_filters.rest_framework.CharFilter(
        method='order_by_func')

    # 标题，简介，标签的联合like查询，不区分大小写
    def order_by_func(self, queryset, name, value):
        return queryset.order_by(value)
    

    class Meta:
        model = Article
        fields = {
            'id': ['exact', 'in'],
            'modify_time': ['exact', 'in','gte','lte'],
            'is_delete': ['exact', 'in'],
        }


class CommentFilter(django_filters.rest_framework.FilterSet):


    order_by =  django_filters.rest_framework.CharFilter(
        method='order_by_func')

    # 标题，简介，标签的联合like查询，不区分大小写
    def order_by_func(self, queryset, name, value):
        return queryset.order_by(value)
    

    class Meta:
        model = Comment
        fields = {
            'id': ['exact', 'in'],
            'article': ['exact', 'in'],
            'is_delete': ['exact', 'in'],
            'modify_time': ['exact', 'in','gte','lte']
        }


