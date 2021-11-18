from rest_framework.serializers import ModelSerializer

from douyin.models import DouYinUser


class DouYinUserSerializer(ModelSerializer):
    class Meta:
        model = DouYinUser
        fields = ('fens_count',)

    def update(self, instance, validated_data):
        print(validated_data)
        return super(DouYinUserSerializer, self).update(instance, validated_data=validated_data)
