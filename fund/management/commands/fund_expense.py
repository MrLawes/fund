from django.core.management.base import BaseCommand

from fund.models import Fund, FundValue, FundExpense


class Command(BaseCommand):
    def handle(self, *_, **options):
        data = {
            '工银瑞信新能源汽车主题混合C': {
                '交易流水': {
                    '2021-10-23': 10,
                }
            },
            "农银汇理": {
                '交易流水': {
                    '2021-11-05': 10,
                }
            },
        }
        for fund_name in data:
            fund = Fund.objects.get(name=fund_name)
            交易流水 = data[fund_name]['交易流水']
            for date in 交易流水:
                fund_value = FundValue.objects.get(fund=fund, deal_at=date)
                hold = FundExpense.get_hold(fund_value=fund_value.value, expense=交易流水[date], fee=fund.fee)
                defaults = {'expense': 交易流水[date], 'hold': hold}
                FundExpense.objects.update_or_create(fund=fund, deal_at=date, defaults=defaults)
