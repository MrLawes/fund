import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from fund.models import Fund
from fund.models import FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):

        # 一年前的 1 月份开始模拟
        start = timezone.localdate() - datetime.timedelta(days=365)

        up_percentage = 1.05  # 涨幅
        down_percentage = 0.95  # 跌幅

        for fund in Fund.objects.all():

            profit = 0

            first_fund_value = FundValue.objects.filter(fund=fund, deal_at__gt=start).first()
            transactions = [
                {"value": first_fund_value.value, "hold": round(10000 / first_fund_value.value, 2)},
            ]
            print(f"{transactions=}")
            for fund_value in FundValue.objects.filter(fund=fund, deal_at__gt=start):
                transaction = transactions[-1]

                if fund_value.value > transaction["value"] * up_percentage:  # todo chenhaiou 卖

                    print(f"{fund_value.fund.name=};{fund_value}")
                    print(f"卖 {transactions=}")

                    sell = transactions.pop()
                    profit += fund_value.value * sell["hold"] - 10000
                    if not transactions:
                        transactions.append({"value": fund_value.value, "hold": round(10000 / fund_value.value, 2)})

                    # transaction = transactions[0]
                    print(f"{profit=}")
                    print(f"卖 {transactions=}")
                    # input()

                elif fund_value.value < transaction["value"] * down_percentage:  # todo chenhaiou 买

                    print(f"{fund_value.fund.name=};{fund_value}")
                    transactions.append({"value": fund_value.value, "hold": round(10000 / fund_value.value, 2)})

                    # transaction = transactions[0]
                    print(f"买 {transactions=}")
                    # input()

            print(f"{fund.name=};{profit=}")
            input()
