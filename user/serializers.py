from rest_framework import serializers

from skill_be.utils.myclass import DynamicFieldsModelSerializer
from user.models import User


class UserSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1
        