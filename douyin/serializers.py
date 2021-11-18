from rest_framework.serializers import ModelSerializer

from douyin.models import DouYinUser


class DouYinUserSerializer(ModelSerializer):
    class Meta:
        model = DouYinUser
        fields = ('fens_count',)
