import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from fund.models import Fund
from fund.models import FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):

        def calculate_fund_growth(initial_nav, final_nav, initial_investment):
            shares = initial_investment / initial_nav
            final_value = shares * final_nav
            profit = final_value - initial_investment
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

        localtime = timezone.localtime() - datetime.timedelta(days=365)
        data = {}
        for fund in Fund.objects.all():
            before = FundValue.objects.filter(fund=fund, deal_at__gt=localtime).first()
            values = []
            results = []
            data.setdefault(fund.name, {"涨": 0, "总收益": 0, })
            for value in FundValue.objects.filter(fund=fund, deal_at__gt=localtime):
                values.append(value.value)
                if value.value > before.value:
                    result = calculate_fund_growth(before.value, value.value, 10000)
                    data[fund.name]["总收益"] += result["总收益"]
                    results.append("涨")
                else:
                    results.append("跌")
                before = value

        sorted_data_asc = sorted(data.items(), key=lambda x: x[1]['总收益'], reverse=True)

        # 输出结果
        for fund_name, value in sorted_data_asc:
            print(f"{fund_name}: {value['总收益']}")

        """
        [半导体]诺安成长混合: 19160.239462510297
        [医疗]工银瑞信前沿医疗股票C: 14984.296089772175
        [新能源]工银瑞信新能源汽车主题混合C: 14967.207651866463
        [军工]易方达国防军工混合C: 13465.840334440998
        [白酒]招商中证白酒指数C: 10424.688971449035
        [黄金]博时黄金ETF联接C: 1397.1352130184132
        """
