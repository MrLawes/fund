import datetime  # noqa

from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from fund.models import FundExpense
from fund.serializers import FundExpenseSerializer


class FundExpenseViewSet(ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = FundExpense.objects.all()
    serializer_class = FundExpenseSerializer

    @action(methods=['get'], detail=True, )
    def sale(self, request, version, pk):  # noqa
        fund_expense = self.get_object()
        fund_expense.expense_type = 'sale'
        fund_expense.save()
        referer = request.headers['Referer']
        return HttpResponseRedirect(referer)
