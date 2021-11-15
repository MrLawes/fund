from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from fund.models import Fund


class FundSerializer(ModelSerializer):
    pyramid = serializers.SerializerMethodField(read_only=True, help_text='金字塔', )

    class Meta:
        model = Fund
        fields = ('pyramid',)

    def get_pyramid(self, fund):
        return """<hr width="10%" /><hr width="20%"/><hr width="30%"/><hr width="40%"/><hr width="50%"/><hr width="60%"/><hr width="70%"/><hr width="80%"/><hr width="90%"/><hr width="100%"/>"""
