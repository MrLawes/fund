import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand

from fund.models import Fund, FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):

        fund = Fund.objects.get(name="[白酒]招商中证白酒指数C")
        before = FundValue.objects.filter(fund=fund).first()
        values = []
        results = []
        for value in FundValue.objects.filter(fund=fund):
            values.append(value.value)
            if value.value > before.value:
                # if 是否上涨:
                #     上涨次数 += 1
                # else:
                #     连续上涨次数.setdefault(上涨次数)
                #     连续上涨次数[下跌次数] += 1
                print(f"↑ {value=};{before=}")
                # results.append("↑")
                results.append("涨")
            else:
                # if not 是否上涨:
                #     下跌次数 += 1
                # else:
                #
                #     连续下跌次数.setdefault(下跌次数)
                #     连续下跌次数[下跌次数] += 1
                print(f"↓ {value=};{before=}")
                results.append("跌")
                # results.append("↓")
            before = value

        def count_consecutive_trends(prices):
            """
            统计连续上涨和连续下跌的次数

            Args:
                prices: 价格趋势列表，包含'涨'和'跌'

            Returns:
                tuple: (连续上涨次数统计, 连续下跌次数统计)
            """
            consecutive_up = {}  # 连续上涨次数统计
            consecutive_down = {}  # 连续下跌次数统计

            i = 0
            while i < len(prices):
                if prices[i] == '涨':
                    # 计算连续上涨次数
                    count = 0  # noqa
                    while i < len(prices) and prices[i] == '涨':
                        count += 1
                        i += 1
                    if count > 0:
                        consecutive_up[count] = consecutive_up.get(count, 0) + 1
                elif prices[i] == '跌':
                    # 计算连续下跌次数
                    count = 0  # noqa
                    while i < len(prices) and prices[i] == '跌':
                        count += 1
                        i += 1
                    if count > 0:
                        consecutive_down[count] = consecutive_down.get(count, 0) + 1
                else:
                    i += 1

            return consecutive_up, consecutive_down

        # print(f"{results=}")

        # 统计连续涨跌次数
        up_counts, down_counts = count_consecutive_trends(results)

        # 准备饼图数据
        up_labels = [f'u {times}' for times in sorted(up_counts.keys())]
        up_sizes = [up_counts[times] for times in sorted(up_counts.keys())]
        down_labels = [f'd {times}' for times in sorted(down_counts.keys())]
        down_sizes = [down_counts[times] for times in sorted(down_counts.keys())]

        # 创建饼图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # 连续上涨饼图
        if up_sizes:
            ax1.pie(up_sizes, labels=up_labels, autopct='%1.1f%%', startangle=90)
            ax1.set_title('up')

        # 连续下跌饼图
        if down_sizes:
            ax2.pie(down_sizes, labels=down_labels, autopct='%1.1f%%', startangle=90)
            ax2.set_title('down')

        plt.tight_layout()

        print(f"{fund.name}, 连续上涨次数统计:")
        for times, count in sorted(up_counts.items()):
            print(f"  连续涨 {times} 次: {count} 次")

        print("\n连续下跌次数统计:")
        for times, count in sorted(down_counts.items()):
            print(f"  连续跌 {times} 次: {count} 次")

        plt.show()
