import uuid

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from douyin.models import DouYinUser


class DouYinUserSerializer(ModelSerializer):
    username = serializers.CharField(help_text='抖音号', default=uuid.uuid4)
    create_at = serializers.DateTimeField(help_text='创建时间', read_only=True)

    class Meta:
        model = DouYinUser
        fields = (
            'id', 'username', 'first_name', 'href', 'fens_count', 'relationship', 'follow_count', 'head_url',
            'create_at',)

    def create(self, validated_data):
        print(f'{validated_data=}')
        if DouYinUser.objects.filter(href=validated_data['href']).exists():
            DouYinUser.objects.filter(href=validated_data['href']).update(relationship=validated_data['relationship'])
            return Response()
        if not 'username' in validated_data:
            validated_data['username'] = uuid.uuid4()
        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        # print(f"{validated_data=}")
        validated_data['username'] = validated_data.get('username', instance.username)
        validated_data['username'] = validated_data['username'].replace('抖音号： ', '')
        return super().update(instance=instance, validated_data=validated_data)
