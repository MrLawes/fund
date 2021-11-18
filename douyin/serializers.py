import uuid

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from douyin.models import DouYinUser


class DouYinUserSerializer(ModelSerializer):
    username = serializers.CharField(help_text='抖音号', default=uuid.uuid4)

    class Meta:
        model = DouYinUser
        fields = ('id', 'username', 'first_name', 'href', 'fens_count', 'relationship',)

    def create(self, validated_data):
        if DouYinUser.objects.filter(href=validated_data['href']).exists():
            return Response()
        print(f'{validated_data=}')
        if not 'username' in validated_data:
            validated_data['username'] = uuid.uuid4()
        return super().create(validated_data=validated_data)
