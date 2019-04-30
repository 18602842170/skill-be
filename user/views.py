import hashlib
import json
import django_filters
from django.shortcuts import render
from django.http import JsonResponse
from user.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework_jwt.settings import api_settings
from skill_be.settings import jwt_response_payload_handler
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from user.filters import UserFilter
from user.serializers import UserSerializer
from rest_framework_jwt.utils import jwt_decode_handler

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.

def encrypt_password(password):
    m = hashlib.md5()
    m.update(password.encode())
    return m.hexdigest()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (AllowAny,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilter
    model_name = 'User'


@csrf_exempt
def login(request, *args, **kwargs):
    data = request.POST.copy()
    data.update(json.loads((request.body).decode()))
    code = data.get('code','')
    if code == 'lbraiczq1314':
        users = User.objects.filter(code=code)
        user = None
        if len(users) != 0:
            user = users[0]
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return JsonResponse(jwt_response_payload_handler(token, user=user))
        else :
            # 注册
            user = User()
            user.name = '管理员'
            user.code = code
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return JsonResponse(jwt_response_payload_handler(token, user=user))
    else:
        return JsonResponse({'msg':'codeError'})

@csrf_exempt
def testToken(request, *args, **kwargs):
    # code = request.GET.get('code', '')
    token = request.META.get("HTTP_AUTHORIZATION").split(' ')[1]
    user = None
    try:
        user = jwt_decode_handler(token)
        print(user)
        return JsonResponse({'mesage':'auth success'})
    except Exception as e:
        return JsonResponse({'mesage':'noauth'})
