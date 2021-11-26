import datetime

from django.core.management.base import BaseCommand
from tabulate import tabulate

from fund.models import Fund, FundValue, FundExpense


class Command(BaseCommand):
    def handle(self, *_, **options):
        data = {
            "[半导体]华夏国证半导体芯片ETF联接C": {  # 上涨中
                '三年年化': 300,
                "交易规则": '大于7天：0%',
                "高抛低吸": True,
                '交易流水': [
                ],
            },
            "[白酒]招商中证白酒指数C": {  # 上涨中
                '三年年化': 268,
                '交易流水': [
                ],
                "交易规则": '大于7天：0%',
                "高抛低吸": True,
            },
            "[医疗]工银前沿医疗股票C": {  # 上涨中
                '三年年化': 209,
                "交易规则": '大于30天: 0%',
                "高抛低吸": True,
                '交易流水': [
                ],
            },
            "[军工]鹏华空天军工指数(LOF)C": {  # 下跌中
                '交易流水': [
                    ('2021-11-24', 10),
                ],
                '三年年化': 188,
                "交易规则": '大于7天：0%',
                "高抛低吸": True,
            },
            "[新能源]工银瑞信新能源汽车主题混合C": {  # 下跌中
                '三年年化': 337,
                "交易规则": '大于30天: 0%',
                "高抛低吸": True,
                '交易流水': [('2021-10-23', 10.0), ('2021-11-24', 130.0), ('2021-11-25', 130.0)],
            },
            ########################### 高抛低吸分割线 ###########################

            '[白酒]招商中证白酒指数(LOF)A': {  # todo chenhaiou 缺差 7.03 份
                '三年年化': 294,
                '交易流水': [
                    ('2021-10-18', 812.8,),
                    ('2021-10-27', 665.01,),
                    ('2021-11-09', 118.06,),
                    ('2021-11-11', 1420.29 + 9.051125,),
                ],
                "交易规则": '大于7天：0.5%',
            },
            '[半导体]诺安成长混合': {
                '三年年化': 300,
                '交易流水': [
                    ('2021-08-06', 10.0),
                    ('2021-08-10', 990.23),
                    ('2021-08-30', 139.09),
                    ('2021-09-16', 479.68),
                    ('2021-09-29', 482.49),
                    ('2021-10-11', 520.49),
                    ('2021-10-12', 539.0),
                    ('2021-10-18', 434.94),
                    ('2021-10-20', 79.79),
                    ('2021-10-27', 586.66)
                ],
                "交易规则": '大于7天：0.5%',
            },
            '[半导体]国泰半导体C': {
                '三年年化': 300,
                '交易流水':
                    [('2021-11-03', 700.0), ('2021-11-08', 700.0), ('2021-11-12', 300.0), ('2021-11-18', 130)]
                ,
                "交易规则": '大于30天：0%',
            },
            "[医疗]中欧医疗C": {
                '三年年化': 209,
                "交易规则": '大于30天: 0.5%',
                '交易流水': [('2021-11-18', 260.0)],
            },
            "[医疗]中欧医疗A": {
                '交易流水': [('2021-08-05', 10.0), ('2021-08-08', 990.29), ('2021-08-11', -33.03), ('2021-08-28', 249.5),
                         ('2021-09-29', 274.29), ('2021-10-20', 473.17), ('2021-10-14', 500.0), ('2021-10-11', 511.6),
                         ('2021-10-18', 569.48), ('2021-10-26', 543.6), ('2021-10-27', 543.96), ('2021-11-01', 976.81),
                         ('2021-11-04', 500.0), ('2021-11-08', 700.0), ('2021-11-12', 486.42)],
                '三年年化': 209,
                "交易规则": '大于30天: 0.5%',
            },
            '[新能源]农银工业4.0混合': {
                '三年年化': 431,
                '交易流水': [
                    ('2021-11-05', 10.0), ('2021-11-25', 120.0),
                ],
                "交易规则": '大于30天: 0.5%',
            },
            "[军工]易方达国防军工混合": {
                '交易流水': [
                    ('2021-11-23', 130),
                ],
                '三年年化': 188,
                "交易规则": '大于30天: 0.5%',
            },
            # "[混合]易方达蓝筹精选": {
            #     'N年年化': [159., 3 * 12 * 30],
            #     "交易规则": '',
            #     '交易流水': [
            #     ],
            # },
        }
        for fund_name in data:
            fund = Fund.objects.get(name=fund_name)
            FundExpense.objects.filter(fund=fund).delete()
            fund.three_yearly_change = data[fund_name]['三年年化']
            fund.transaction_rule = data[fund_name]['交易规则']
            fund.high_sale_low_buy = data[fund_name].get('高抛低吸', False)
            fund.save()
            交易流水 = data[fund_name]['交易流水']
            for detail in 交易流水:
                fund_value = FundValue.objects.get(fund=fund, deal_at=detail[0])
                hold = FundExpense.get_hold(fund_value=fund_value.value, expense=detail[1], fee=fund.fee)
                defaults = {'expense': detail[1], 'hold': hold}
                FundExpense.objects.update_or_create(fund=fund, deal_at=detail[0], defaults=defaults)

        # 输出结果
        tabular_data, headers = [], ['持有份数', '  投入金额/持有市值/期望市值', '      持有收益/期望收益', '         持有收益率/期望收益率',
                                     '             基金名称', ]
        for 基金名称 in data:
            if not data[基金名称].get('高抛低吸', False):
                continue
            fund = Fund.objects.get(name=基金名称)
            持有市值 = 投入金额 = 期望市值 = 持有份数 = 0
            last_fundvalue = FundValue.objects.filter(fund=fund).exclude(
                deal_at=datetime.datetime.now().date()).order_by(
                'deal_at').last()
            for fund_expense in FundExpense.objects.filter(fund=fund):
                持有市值 += fund_expense.hold * last_fundvalue.value
                持有份数 += fund_expense.hold
                投入金额 += fund_expense.expense
                期望市值 += fund_expense.hope_value
            持有市值 = round(持有市值, 2)
            持有收益 = 持有市值 - 投入金额
            期望收益 = 期望市值 - 投入金额
            持有收益率 = 持有收益 / 投入金额 if 投入金额 > 0 else 0
            期望收益率 = 期望收益 / 投入金额 if 投入金额 > 0 else 0

            if 持有市值 > 期望市值:
                持有市值 = f'\033[0;30;41m{持有市值}\033[0m'
            else:
                持有市值 = f'\033[0;30;42m{持有市值}\033[0m'

            t_data = [
                持有份数,
                f"{投入金额}/{持有市值}/{期望市值:0.02f}",
                f"{持有收益:0.2f}/{期望收益:0.02f}",
                f"{(持有收益率 * 100):0.02f}%/{(期望收益率 * 100):0.02f}%",
                基金名称,
            ]
            tabular_data.append(t_data)

        print(tabulate(tabular_data=tabular_data, headers=headers, numalign='left'))
