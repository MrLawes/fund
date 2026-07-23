import datetime

import requests
from django.core.management.base import BaseCommand
from rich.console import Console
from rich.table import Table
from tabulate import tabulate

from fund.management.commands.simulate_trades import Command as SimulateTradesCommand
from fund.models import Fund
from fund.models import FundExpense
from fund.models import FundHoldings
from fund.models import FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        now = datetime.datetime.now()
        # end_date = datetime.datetime.now()
        # start_date = (end_date - datetime.timedelta(days=15)).strftime('%Y-%m-%d')
        # end_date = end_date.strftime('%Y-%m-%d')

        # 首页: https://fund.10jqka.com.cn/
        for fund in Fund.objects.all().order_by('name'):

            url = f"https://fund.10jqka.com.cn/data/client/myfund/{fund.code}"
            r = requests.get(url=url, headers=headers, timeout=40)
            result = r.json()['data'][0]
            # 更新昨天的数据
            defaults = {'value': result['net'], 'rate': result['rate']}
            deal_at = result['enddate']
            FundValue.objects.update_or_create(fund=fund, deal_at=deal_at, defaults=defaults)

            # 查看最新估值: https://finance.sina.com.cn/fund/quotes/008888/bc.shtml
            today_data = {
                "2026-07-23": {
                    '008888': {'value': 2.1258, },  # 半导体
                    '010364': {'value': 0.8958, },  # 军工
                    '022653': {'value': FundValue.objects.filter(fund__code='022653', deal_at__lte=deal_at).order_by(
                        'deal_at').last().value * (0.68 / 100) + 1, },  # 黄金
                    '010685': {'value': 3.2950, },  # 医疗
                    '003095': {'value': 2.0019, },  # 医疗A
                    '012414': {'value': 0.5470, },  # 白酒
                }
            }
            if now.strftime('%Y-%m-%d') in today_data:
                t_data = today_data[now.strftime('%Y-%m-%d')]

                # 更新今天的数据
                if fund.code in t_data:
                    today_value = t_data[fund.code]['value']
                    rate = (today_value - float(result['net'])) / float(result['net']) * 100
                    defaults = {'value': today_value, 'rate': f"{rate:0.02f}"}
                    FundValue.objects.update_or_create(
                        fund=fund,
                        deal_at=datetime.datetime.now().strftime('%Y-%m-%d'),
                        defaults=defaults
                    )

            newest_fund_value = FundValue.objects.filter(fund=fund).order_by('deal_at').last()
            if newest_fund_value:
                fund.newest_rate = newest_fund_value.rate
                fund.save()

            # url = f'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode={fund.code}&startdate={start_date}&enddate={end_date}'
            # print(f'{fund.name}: {url=}')
            # try:
            #     r = requests.get(url=url, headers=headers, timeout=10)
            # except:  # noqa
            #     continue
            # content = str(r.content)
            # print(f"{content=}")
            # content_split_list = content.split('<tr>')
            #
            # for content_split in content_split_list:
            #     print(111111111111111)
            #     if not ('class="f_green"' in content_split or 'class="f_red"' in content_split):
            #         continue
            #     print(22222222222222222222)
            #     td_split = content_split.split('</td>')
            #     date = td_split[0].split('>')[-1]
            #     if not date:
            #         continue
            #     print(333333333333333333333333333)
            #     value = td_split[1].split('>')[-1]
            #     rate = float(td_split[3].split('>')[-1].replace('%', ''))
            #
            #     defaults = {'value': value, 'rate': rate}
            #     FundValue.objects.update_or_create(fund=fund, deal_at=date, defaults=defaults)

            # 获得最新的净值数据
            last_fundvalue = FundValue.objects.filter(fund=fund).order_by('deal_at').last()
            # 将最新的净值数据，更新到所有的交易记录，方便计算
            FundExpense.objects.filter(fund=fund).update(newest_value=last_fundvalue.value)

        fund_categories: list = SimulateTradesCommand().handle()["fund_categories"]
        # 计算持有仓位占比
        FundHoldings.objects.all().delete()
        for fe in FundExpense.objects.all():
            # 更新所有交易的持有收益率，用于排序
            if fe.need_buy_again:
                fe.hold_rate = 0
            else:
                if fe.expense == 0:
                    fe.hold_rate = 0
                else:
                    fe.hold_rate = ((((fe.hold * fe.newest_value) - fe.expense) / fe.expense) * 100)
            fe.save(update_fields=['hold_rate', ])

            # 计算投资回报的年化率
            fe.set_annual_interest_rate()

            if fe.fund.name in (
                    '[白酒]招商中证白酒指数C',
                    "[军工]鹏华空天军工指数(LOF)C",
                    "[医疗]工银瑞信前沿医疗股票C",
                    "[黄金]华安黄金ETF联接I",
                    "[债券]博时裕新纯债债券C",
                    "[半导体]华夏国证半导体芯片ETF联接C",
            ):
                if fe.fund.name == "[医疗]工银瑞信前沿医疗股票C":
                    if fe.id < 4400:
                        continue

                fund_value = FundValue.objects.get(fund=fe.fund, deal_at=fe.deal_at)
                fee = fe.fund.fee
                expense = fe.expense
                hold = FundExpense.get_hold(fund_value=fund_value.value, expense=expense, fee=fee)
                if fe.expense_type == 'buy':
                    fe.hold = hold
                fe.save(update_fields=['hold', ])

            # 计算持有仓位占比
            catetory_name = fe.fund.name.split(']')[0].split('[')[-1]
            fund_holdings, _ = FundHoldings.objects.get_or_create(catetory_name=catetory_name)
            if fe.expense_type == 'buy':
                fund_holdings.hold += fe.hold
                fund_holdings.expense += fe.expense
            elif fe.expense_type == 'sale':
                fund_holdings.hold -= fe.hold
                fund_holdings.expense -= fe.expense
            fund_holdings.save()

        table = Table(title="")
        headers = ['ID', '交易日期', '基金名称', '确认份额', '确认金额', '持有市值', "估算涨幅", ]
        for header in headers:
            table.add_column(header, no_wrap=True)

        tabulate_table = []

        for fund_category in dict(Fund.FUND_CATEGORY).values():
            if fund_category not in fund_categories:
                fund_categories.append(fund_category)

        for fund_category in fund_categories:
            for fund_expense in FundExpense.objects.filter(
                fund__name__contains=f"[{fund_category}]",
                expense_type='buy',
                need_buy_again=False).order_by('-hold_rate')[:9]:
                last_fundvalue = FundValue.objects.filter(fund=fund_expense.fund).order_by('deal_at').last()
                value = round(fund_expense.hold * last_fundvalue.value, 2)
                if fund_expense.expense == 0:
                    fund_value = fund_expense.fund_value
                    hold_rate_persent = f"{(((last_fundvalue.value - fund_value.value) / fund_value.value) * 100):0.02f}%"
                else:
                    hold_rate_persent = f"{(((value - fund_expense.expense) / fund_expense.expense) * 100):0.02f}%"
                if "-" in hold_rate_persent:
                    hold_rate_persent = f"{hold_rate_persent}({(fund_expense.fund.buy_percentage - 1) * 100:0.02f}%)"
                else:
                    hold_rate_persent = f"{hold_rate_persent}({(fund_expense.fund.sell_percentage - 1) * 100:0.02f}%)"
                table.add_row(
                    f'{fund_expense.id}',
                    f'{fund_expense.deal_at}',
                    f'{fund_expense.fund.name}({fund_expense.fund.code})',
                    f'{fund_expense.hold}',
                    f'{fund_expense.expense}',
                    f'{hold_rate_persent}',
                    f"{last_fundvalue.rate}",
                )
                tabulate_table.append([
                    f'{fund_expense.id}',
                    f'{fund_expense.deal_at}',
                    f'{fund_expense.fund.get_category_display()}',
                    f'{fund_expense.hold}',
                    f'{fund_expense.expense}',
                    f'{hold_rate_persent}',
                    f"{last_fundvalue.rate}",
                ])
            table.add_row(
                f'---',
                f'---',
                f'---',
                f'---',
                f'---',
                f'---',
                f'---',
            )
            tabulate_table.append([
                f'---',
                f'---',
                f'---',
                f'---',
                f'---',
                f'---',
                f'---',
            ])

        console = Console()
        console.print(table)
        print('\n\n\n\n\n\n\n\n\n\n\n\n')

        ret = tabulate(tabulate_table, headers=headers)

        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "content": f"❗️待审核通知",
                        "tag": "plain_text"
                    },
                    "template": "red",
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": ret,
                            "tag": "lark_md",
                        }
                    },
                ],
            }
        }
        requests.post(
            'https://open.feishu.cn/open-apis/bot/v2/hook/ad6706f4-2667-4786-8ba1-fcf483101b38',
            json=payload,
            timeout=5,
            verify=False,  # 禁用 SSL 验证
        )
