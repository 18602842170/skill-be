from django.db import models
from user.models import User
from django.contrib.postgres.fields.jsonb import JSONField
# Create your models here.
class Article(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50, default='')
    outline = models.CharField(verbose_name='简介', max_length=500, default='')
    readCount = models.IntegerField(verbose_name='阅读次数', default=0)
    label = models.CharField(verbose_name='标签', max_length=100, default='')
    content=  JSONField(verbose_name='内容',default=[])   
    create_time = models.DateTimeField(
    verbose_name='创建时间', auto_now_add=True, null=True)
    modify_time = models.DateTimeField(
        verbose_name='更新时间', null=True, auto_now=True)
    is_delete = models.BooleanField(verbose_name='删除标记', default=False)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return 'id:' + str(self.id)


class Comment(models.Model):
    message = models.CharField(verbose_name='评论内容', max_length=500, default='')
    rate = models.FloatField(verbose_name='评分', default=3)
    likes = models.IntegerField(verbose_name='评论点赞次数', default=0)
    dislikes = models.IntegerField(verbose_name='评论不喜欢次数', default=0)
    article = models.ForeignKey(
        Article, related_name='article_comments', null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(
    verbose_name='创建时间', auto_now_add=True, null=True)
    modify_time = models.DateTimeField(
        verbose_name='更新时间', null=True, auto_now=True)
    is_delete = models.BooleanField(verbose_name='删除标记', default=False)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return 'id:' + str(self.id)