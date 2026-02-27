import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from fund.models import Fund
from fund.models import FundValue


class Command(BaseCommand):
    def handle(self, *_, **options) -> dict:

        results = {}

        # 一年前的 1 月份开始模拟
        start = timezone.localdate() - datetime.timedelta(days=32)
        for fund in Fund.objects.all():
            if fund.category == 7:
                continue
            for up_extent in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15,
                              0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28,):
                for down_extent in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14,
                                    0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27,
                                    0.28,):
                    too_lot = False
                    up_percentage = 1 + up_extent  # 涨幅
                    down_percentage = 1 - down_extent  # 跌幅
                    profit = 0
                    first_fund_value = FundValue.objects.filter(fund=fund, deal_at__gt=start).first()
                    if not first_fund_value:
                        continue
                    transactions: list[dict] = [
                        {"value": first_fund_value.value, "hold": round(10000 / first_fund_value.value, 2)},
                    ]
                    # print(f"交易记录: {fund.name} {transactions=}")
                    for fund_value in FundValue.objects.filter(fund=fund, deal_at__gt=start):
                        transaction = transactions[-1]

                        # if len(transactions) > 5:
                        #     too_lot = True
                        #     break

                        if fund_value.value > transaction["value"] * up_percentage:

                            # if len(transactions) <= 1:
                            #     continue

                            # print(f"卖 净值:{fund_value.value}")
                            sell = transactions.pop()
                            profit += fund_value.value * sell["hold"] - 10000
                            if not transactions:
                                transactions.append(
                                    {"value": fund_value.value, "hold": round(10000 / fund_value.value, 2)})
                            # print(f"盈利: {profit=}")
                            # print(f"交易记录: {fund.name} {transactions=}")

                        elif fund_value.value < transaction["value"] * down_percentage:
                            # print(f"买 净值:{fund_value.value}")
                            transactions.append({"value": fund_value.value, "hold": round(10000 / fund_value.value, 2)})
                            # print(f"交易记录: {fund.name} {transactions=}")

                    if too_lot:
                        continue

                    # print(f"{fund.name=};{profit=}")
                    results.setdefault(fund.name, [])
                    results[fund.name].append(
                        {
                            "profit": profit, "up_percentage": up_percentage, "down_percentage": down_percentage,
                            "name": fund.name, "fund_id": fund.id,
                        }
                    )

        best_results = []

        for fund_name, result in results.items():

            best_profit = 0
            best_data = {}
            for item in result:
                if item['profit'] > best_profit:
                    best_profit = item['profit']
                    best_data = item

            if best_data:
                best_results.append(best_data)
                fund = Fund.objects.get(id=best_data['fund_id'])
                fund.sell_percentage = best_data['up_percentage']
                fund.buy_percentage = best_data["down_percentage"]
                fund.save(update_fields=['sell_percentage', 'buy_percentage'])

        best_results = sorted(best_results, key=lambda x: x['profit'], reverse=True)
        fund_categories = []
        for best_data in best_results:
            fund_category = best_data["name"]
            fund_category = fund_category.split("]")[0].split("[")[1]
            if fund_category not in fund_categories:
                fund_categories.append(fund_category)
            print(f"{best_data=}")

        return {
            "fund_categories": fund_categories,
        }
