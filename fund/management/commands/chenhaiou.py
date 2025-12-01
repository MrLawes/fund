from django.core.management.base import BaseCommand
from django.utils import timezone

from fund.models import Fund
from fund.models import FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):

        def calculate_fund_growth(initial_nav, final_nav, initial_investment):
            """
            计算基金净值增长后的收益情况

            Args:
                initial_nav: 初始净值
                final_nav: 最终净值
                initial_investment: 初始投资金额

            Returns:
                dict: 包含收益信息的字典
            """
            # 计算份额
            shares = initial_investment / initial_nav

            # 计算最终价值
            final_value = shares * final_nav

            # 计算收益
            profit = final_value - initial_investment

            # 计算收益率
            profit_rate = (final_nav - initial_nav) / initial_nav * 100

            return {
                "初始净值": initial_nav,
                "最终净值": final_nav,
                "初始投资": initial_investment,
                "获得份额": shares,
                "最终价值": final_value,
                "总收益": profit,
                "收益率": f"{profit_rate:.2f}%"
            }

        now = timezone.localtime()
        data = {}
        for fund in Fund.objects.all():
            # fund = Fund.objects.get(name="[新能源]工银瑞信新能源汽车主题混合C")
            before = FundValue.objects.filter(fund=fund, deal_at__year=now.year).first()
            values = []
            results = []
            data.setdefault(fund.name, {"涨": 0, "总收益": 0, })
            for value in FundValue.objects.filter(fund=fund, deal_at__year=now.year):
                values.append(value.value)
                if value.value > before.value:
                    # data[fund.name]["涨"] += value.value - before.value
                    result = calculate_fund_growth(before.value, value.value, 10000)
                    data[fund.name]["总收益"] += result["总收益"]

                    # if 是否上涨:
                    #     上涨次数 += 1
                    # else:
                    #     连续上涨次数.setdefault(上涨次数)
                    #     连续上涨次数[下跌次数] += 1

                    # print(f"↑ {value=};{before=};{data=}")
                    # print(f"↑ {result=}")
                    # input()
                    # results.append("↑")
                    results.append("涨")
                else:
                    # if not 是否上涨:
                    #     下跌次数 += 1
                    # else:
                    #
                    #     连续下跌次数.setdefault(下跌次数)
                    #     连续下跌次数[下跌次数] += 1
                    # print(f"↓ {value=};{before=}")
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
                consecutive_last = {}  # noqa

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
                            consecutive_last = {"涨": count}  # noqa
                    elif prices[i] == '跌':
                        # 计算连续下跌次数
                        count = 0  # noqa
                        while i < len(prices) and prices[i] == '跌':
                            count += 1
                            i += 1
                        if count > 0:
                            consecutive_down[count] = consecutive_down.get(count, 0) + 1
                            consecutive_last = {"跌": count}  # noqa
                    else:
                        i += 1

                return consecutive_up, consecutive_down, consecutive_last
            #
            # # print(f"{results=}")
            #
            # # 统计连续涨跌次数
            # up_counts, down_counts, consecutive_last = count_consecutive_trends(results)
            #
            # # 准备饼图数据
            # up_labels = [f'u {times}' for times in sorted(up_counts.keys())]
            # up_sizes = [up_counts[times] for times in sorted(up_counts.keys())]
            # down_labels = [f'd {times}' for times in sorted(down_counts.keys())]
            # down_sizes = [down_counts[times] for times in sorted(down_counts.keys())]
            #
            # # 创建饼图
            # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            #
            # # 连续上涨饼图
            # if up_sizes:
            #     ax1.pie(up_sizes, labels=up_labels, autopct='%1.1f%%', startangle=90)
            #     ax1.set_title('up')
            #
            # # 连续下跌饼图
            # if down_sizes:
            #     ax2.pie(down_sizes, labels=down_labels, autopct='%1.1f%%', startangle=90)
            #     ax2.set_title('down')

            # plt.tight_layout()

            # print(f"{fund.name}, 连续上涨次数统计:")
            # for times, count in sorted(up_counts.items()):
            #     print(f"  连续涨 {times} 次: {count} 次")
            # print(f"  涨共计 {results.count('涨')} ({int(results.count('涨') * 100 / len(results))}%)次")

            # print("\n连续下跌次数统计:")
            # for times, count in sorted(down_counts.items()):
            #     print(f"  连续跌 {times} 次: {count} 次")
            # print(f"  跌共计 {results.count('跌')} ({int(results.count('跌') * 100 / len(results))}%)次")
            # print(f"{consecutive_last=}")
            # 0.43 *

        sorted_data_asc = sorted(data.items(), key=lambda x: x[1]['涨'], reverse=True)

        # 输出结果
        for fund_name, value in sorted_data_asc:
            print(f"{fund_name}: {value['总收益']}")

        # sorted_data_asc = sorted(data, key=lambda x: x['涨'])
        # for fund_name, value in sorted_data_asc:
        #     print(f"{fund_name}: {value['涨']}")

        # plt.show()
