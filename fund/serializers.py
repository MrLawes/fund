from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from fund.models import FundExpense


class FundExpenseSerializer(ModelSerializer):
    expense_type = serializers.CharField(help_text='基金交易类型: buy: 购买；sale：出售')

    class Meta:
        model = FundExpense
        fields = ('id', 'expense_type',)
