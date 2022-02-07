import datetime  # noqa
import time

from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fund.admin import FundExpenseForm
from fund.models import FundExpense, FundValue
from fund.serializers import FundExpenseSerializer


class FundExpenseViewSet(ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = FundExpense.objects.all()
    serializer_class = FundExpenseSerializer

    @action(methods=['get'], detail=True, )
    def sale(self, request, version, pk):  # noqa
        with transaction.atomic():
            fund_expense = self.get_object()
            fund = fund_expense.fund
            now_date = datetime.datetime.now().date()
            hold = fund_expense.hold
            expense = hold * FundValue.objects.get(fund=fund, deal_at=now_date).value
            FundExpense.objects.create(
                fund=fund, deal_at=now_date, expense=expense, hold=hold, expense_type='sale', sale_at=now_date,
            )
            fund_expense.need_buy_again = True
            fund_expense.save()
            referer = request.headers['Referer']
            return HttpResponseRedirect(referer)

    @action(methods=['get'], detail=True, )
    def buy_again(self, request, version, pk):  # noqa

        with transaction.atomic():
            fund_expense = self.get_object()
            fund_expense.is_buy_again = True
            fund_expense.need_buy_again = False
            fund_expense.save()
            fund_expense_form = FundExpenseForm()
            fund_value = FundValue.objects.filter(fund=fund_expense.fund).last()
            fund_expense_form.cleaned_data = {
                'fund': fund_expense.fund, 'deal_at': f'{datetime.datetime.now().date()}',
                'expense': fund_expense.hold * fund_value.value
            }
            cleaned_data = fund_expense_form.clean()
            FundExpense.objects.create(**cleaned_data)
            referer = request.headers['Referer']
            return HttpResponseRedirect(referer)

    @action(methods=['get'], detail=False, )
    def docker_test(self, request, version, ):  # noqa
        print('11111111')
        for i in range(1, 6):
            time.sleep(1)
        return Response(f"v3:{str(datetime.datetime.now())[:19]}")
