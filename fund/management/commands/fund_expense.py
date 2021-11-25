import datetime

from django.core.management.base import BaseCommand
from tabulate import tabulate

from fund.models import Fund, FundValue, FundExpense


class Command(BaseCommand):
    def handle(self, *_, **options):
        # todo 整理所有的交易
        data = {
            "[军工]鹏华空天军工指数(LOF)C": {
                '交易流水': [
                    ('2021-11-24', 10),
                ],
                'N年年化': [188, 3 * 12 * 30],
                "交易规则": '大于7天：0%',
                "高抛低吸": True,
            },
            # "[军工]易方达国防军工混合": {
            #     '交易流水': [
            #         ('2021-11-23', 130),
            #     ],
            #     'N年年化': [188, 3 * 12 * 30],
            #     "交易规则": '大于30天: 0.5%',
            # },
            # "[医疗]中欧医疗A": {
            #     '交易流水': [
            #         ('2021-11-12', 486.42),
            #     ],
            #     'N年年化': [209, 3 * 12 * 30],
            #     "交易规则": '大于30天: 0.5%',
            # },
            # "[医疗]中欧医疗C": {
            #     'N年年化': [209, 3 * 12 * 30],
            #     "交易规则": '大于30天: 0.5%',
            #     '交易流水': [
            #     ],
            # },
            # "[医疗]工银前沿医疗股票C": {
            #     'N年年化': [209, 3 * 12 * 30],
            #     "交易规则": '大于30天: 0%',
            #     "高抛低吸": True,
            #     '交易流水': [
            #     ],
            # },
            # "[半导体]华夏国证半导体芯片ETF联接C": {
            #     'N年年化': [300, 3 * 12 * 30],
            #     "交易规则": '大于7天：0%',
            #     "高抛低吸": True,
            #     '交易流水': [
            #     ],
            # },
            # '[半导体]诺安成长混合': {
            #     'N年年化': [300, 3 * 12 * 30],
            #     '交易流水': [
            #         ('2021-08-06', 10, 4.09),
            #     ],
            #     "交易规则": '大于7天：0.5%',
            # },
            # '[半导体]国泰半导体C': {
            #     'N年年化': [300, 3 * 12 * 30, ],
            #     '交易流水': [
            #         ('2021-11-18', 65.76,),
            #     ],
            #     "交易规则": '大于30天：0%',
            # },
            # '[白酒]招商中证白酒指数(LOF)A': {
            #     'N年年化': [268, 3 * 12 * 30],
            #     '交易流水': [
            #         ('2021-11-09', 118.06,),
            #     ],
            #     "交易规则": '大于7天：0.5%',
            # },
            # "[白酒]招商中证白酒指数C": {
            #     'N年年化': [268, 3 * 12 * 30],
            #     '交易流水': [
            #     ],
            #     "交易规则": '大于7天：0%',
            #     "高抛低吸": True,
            # },
            # '[新能源]农银工业4.0混合': {
            #     'N年年化': [431, 3 * 12 * 30],
            #     '交易流水': [
            #     ],
            #     "交易规则": '',
            # },
            # "[新能源]工银瑞信新能源汽车主题混合C": {
            #     'N年年化': [337, 3 * 12 * 30],
            #     "交易规则": '',
            #     "高抛低吸": True,
            #     '交易流水': [
            #     ],
            # },
            # "[混合]易方达蓝筹精选": {
            #     'N年年化': [159., 3 * 12 * 30],
            #     "交易规则": '',
            #     '交易流水': [
            #     ],
            # },
        }
        for fund_name in data:
            fund = Fund.objects.get(name=fund_name)
            fund.three_yearly_change = data[fund_name]['N年年化'][0]
            fund.transaction_rule = data[fund_name]['交易规则']
            fund.high_sale_low_buy = data[fund_name].get('高抛低吸', False)
            fund.save()
            交易流水 = data[fund_name]['交易流水']
            for detail in 交易流水:
                print(fund_name, detail)
                fund_value = FundValue.objects.get(fund=fund, deal_at=detail[0])
                hold = FundExpense.get_hold(fund_value=fund_value.value, expense=detail[1], fee=fund.fee)
                defaults = {'expense': detail[1], 'hold': hold}
                FundExpense.objects.update_or_create(fund=fund, deal_at=detail[0], defaults=defaults)


        def income(基金名称, N年年化, 交易流水):
            """
            基金名称:   新能源汽车
            N年年化:    [316.31, 3 * 12 * 30]
            交易流水:   [('2021-10-01', 10), ('2021-10-19', 200),]
            """
            天化, data = (1 + (N年年化[0] / 100.0)) ** (1 / (N年年化[1] * 1.0)) - 1, {}
            交易流水.sort(key=lambda x: x[0])
            总金额 = 总投入 = 0
            开始交易时间 = datetime.datetime.strptime(交易流水[0][0], '%Y-%m-%d')
            交易天数 = (datetime.datetime.now() - 开始交易时间).days
            for 第几天 in range(0, 交易天数 + 1):
                时间 = (开始交易时间 + datetime.timedelta(days=第几天)).strftime('%Y-%m-%d')
                交易流水_slice = [i[:2] for i in 交易流水]
                总投入 += dict(交易流水_slice).get(时间, 0)
                总金额 += 总金额 * 天化 + dict(交易流水_slice).get(时间, 0)
                # print(基金名称, 时间, 第几天, 总金额, 总投入)

            可售 = 总金额 * 1.0065
            期望收益 = 可售 - 总投入
            持有收益率 = 期望收益 / 总投入

            仓位 = f"{(总投入 * 10.0 / 7000):0.3f}"
            try:
                持有份额 = sum([i[2] for i in 交易流水])
            except:
                持有份额 = 0
            return {
                '时间': 时间,
                '总投入': 总投入,
                '可售': 可售,
                '期望收益': 期望收益,
                '持有收益率': 持有收益率,
                '仓位': 仓位,
                '基金名称': 基金名称,
                '持有份额': 持有份额,
            }

        tabular_data, headers = [], ['时间', ' 投入金额/持有市值/恒定市值/期望市值', '       持有收益/期望收益', '          期望收益率',
                                     '            持有仓位',
                                     '             基金名称', ]
        headers_strip = [h.strip() for h in headers]
        for 基金名称 in data:

            result = income(基金名称, data[基金名称]['N年年化'], data[基金名称]['交易流水'], )

            fund = Fund.objects.get(name=fund_name)
            print(f"{result=}")
            持有市值 = 0
            last_fundvalue = FundValue.objects.filter(fund=fund).order_by('deal_at').last()
            for fund_expense in FundExpense.objects.filter(fund=fund):
                持有市值 += fund_expense.hold * last_fundvalue.value
            持有市值 = round(持有市值, 2)
            value = 持有市值

            #
            # fund = Fund.objects.get(name=fund_name)
            # last_fundvalue = FundValue.objects.filter(fund=fund).order_by('deal_at').last()
            # value = round(obj.hold * last_fundvalue.value, 2)

            持有收益 = value * result['持有份额'] - result['总投入']
            持有收益率 = f"{result['持有收益率'] * 100:0.2f}%"

            恒定市值区间 = data[基金名称].get('恒定市值区间')
            if 恒定市值区间 and value:
                if 恒定市值区间[0] <= value <= 恒定市值区间[1]:
                    恒定市值区间差 = (恒定市值区间[1] - 恒定市值区间[0]) / 10.0
                    恒定市值 = (10 - (value - 恒定市值区间[0]) / 恒定市值区间差) * 7000 / 10
            else:
                恒定市值 = 0

            if 持有市值 > result['可售']:
                持有市值 = f'\033[0;30;41m{持有市值}\033[0m'
            else:
                持有市值 = f'\033[0;30;42m{持有市值}\033[0m'

            t_data = [result['时间'], f"{result['总投入']:0.02f}/{持有市值}/{恒定市值:0.02f}/{result['可售']:0.2f}",
                      f"{持有收益:0.2f}/{result['期望收益']:0.2f}",
                      持有收益率, result['仓位'],
                      result['基金名称'], ]
            tabular_data.append(t_data)

        print(tabulate(tabular_data=tabular_data, headers=headers, numalign='left'))
