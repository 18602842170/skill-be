from django.conf.urls import include, url
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from user import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', views.UserViewSet)
urlpatterns = [
    url('', include(router.urls)),
    url(r'^login/$', views.login),
    url(r'^testToken/$', views.testToken),
]