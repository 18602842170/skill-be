from django.conf.urls import include, url
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from article import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'article', views.ArticleViewSet)
router.register(r'comment', views.CommentViewSet)
urlpatterns = [
    url('', include(router.urls)),
]