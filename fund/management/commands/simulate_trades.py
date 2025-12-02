import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from fund.models import Fund
from fund.models import FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):

        results = {}

        # 一年前的 1 月份开始模拟
        start = timezone.localdate() - datetime.timedelta(days=365)
        for fund in Fund.objects.all():
            for up_extent in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10):
                for down_extent in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10):
                    up_percentage = 1 + up_extent  # 涨幅
                    down_percentage = 1 - down_extent  # 跌幅
                    profit = 0
                    first_fund_value = FundValue.objects.filter(fund=fund, deal_at__gt=start).first()
                    transactions = [
                        {"value": first_fund_value.value, "hold": round(10000 / first_fund_value.value, 2)},
                    ]
                    print(f"交易记录: {transactions=}")
                    for fund_value in FundValue.objects.filter(fund=fund, deal_at__gt=start):
                        transaction = transactions[-1]

                        if fund_value.value > transaction["value"] * up_percentage:
                            print(f"卖 净值:{fund_value.value}")
                            sell = transactions.pop()
                            profit += fund_value.value * sell["hold"] - 10000
                            if not transactions:
                                transactions.append(
                                    {"value": fund_value.value, "hold": round(10000 / fund_value.value, 2)})
                            print(f"盈利: {profit=}")
                            print(f"交易记录: {transactions=}")

                        elif fund_value.value < transaction["value"] * down_percentage:
                            print(f"买 净值:{fund_value.value}")
                            transactions.append({"value": fund_value.value, "hold": round(10000 / fund_value.value, 2)})
                            print(f"交易记录: {transactions=}")

                    print(f"{fund.name=};{profit=}")
                    results.setdefault(fund.name, [])
                    results[fund.name].append(
                        {
                            "profit": profit, "up_percentage": up_percentage, "down_percentage": down_percentage,
                            "name": fund.name
                        }
                    )

        # print(f"模拟结果: {json.dumps(results, ensure_ascii=False, indent=4)})")
        for fund_name, result in results.items():

            best_profit = 0
            best_data = {}
            for item in result:
                if item['profit'] > best_profit:
                    best_profit = item['profit']
                    best_data = item

            print(f"模拟最好结果: {best_data=})")
