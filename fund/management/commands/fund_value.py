import datetime
import json

import httpx
import requests
from django.core.management.base import BaseCommand
from rich.console import Console
from rich.table import Table
from tabulate import tabulate

from fund.models import Fund, FundValue, FundExpense, FundHoldings


class Command(BaseCommand):
    def handle(self, *_, **options):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        end_date = datetime.datetime.now()
        start_date = (end_date - datetime.timedelta(days=15)).strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')

        for fund in Fund.objects.all().order_by('name'):
            newest_url = f'http://fundgz.1234567.com.cn/js/{fund.code}.js?rt=1637210892780'
            r = httpx.get(url=newest_url, headers=headers, timeout=40)
            content = json.loads(str(r.content).replace('jsonpgz(', '').replace('\\', '')[2:-3])
            # 更新昨天的数据
            defaults = {'value': content['dwjz'], 'rate': 0}

            # jzrq 有两种格式： 1：2021-12-03；2：21-12-03
            deal_at = content['jzrq']
            if len(deal_at.split('-')[0]) == 2:
                deal_at = '20' + deal_at
            if len(deal_at) == 8:
                deal_at = deal_at[:4] + '-' + deal_at[4:6] + '-' + deal_at[6:]
            FundValue.objects.update_or_create(fund=fund, deal_at=deal_at, defaults=defaults)
            # 更新今天的数据
            defaults = {'value': content['gsz'], 'rate': content['gszzl']}
            FundValue.objects.update_or_create(fund=fund, deal_at=content['gztime'][:10], defaults=defaults)

            newest_fund_value = FundValue.objects.filter(fund=fund).order_by('deal_at').last()
            if newest_fund_value:
                fund.newest_rate = newest_fund_value.rate
                fund.save()

            url = f'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode={fund.code}&startdate={start_date}&enddate={end_date}'
            print(f'{fund.name}: {url=}')
            try:
                r = httpx.get(url=url, headers=headers, timeout=10)
            except:  # noqa
                continue
            content = str(r.content)
            content_split_list = content.split('<tr>')

            for content_split in content_split_list:
                if not ('class="f_green"' in content_split or 'class="f_red"' in content_split):
                    continue
                td_split = content_split.split('</td>')
                date = td_split[0].split('>')[-1]
                if not date:
                    continue
                value = td_split[1].split('>')[-1]
                rate = float(td_split[3].split('>')[-1].replace('%', ''))

                defaults = {'value': value, 'rate': rate}
                FundValue.objects.update_or_create(fund=fund, deal_at=date, defaults=defaults)

            # 获得最新的净值数据
            last_fundvalue = FundValue.objects.filter(fund=fund).order_by('deal_at').last()
            # 将最新的净值数据，更新到所有的交易记录，方便计算
            FundExpense.objects.filter(fund=fund).update(newest_value=last_fundvalue.value)

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
                    '[军工]易方达国防军工混合A',
                    '[半导体]银河创新成长混合C',
                    '[白酒]招商中证白酒指数C',
            ):
                fund_value = FundValue.objects.get(fund=fe.fund, deal_at=fe.deal_at)
                fee = fe.fund.fee
                expense = fe.expense
                hold = FundExpense.get_hold(fund_value=fund_value.value, expense=expense, fee=fee)
                fe.hold = hold

            if fe.id == 3894:
                fe.hold = 410.21
            if fe.id == 3912:
                fe.hold = 1296.57
            if fe.id == 3956:
                fe.hold = 978.37
            if fe.id == 3989:
                fe.hold = 1044.05

            # todo 半导体
            if fe.id == 3920:
                fe.hold = 348.03

            # todo 军工
            if fe.id == 3892:
                fe.hold = 593.12
            if fe.id == 3950:
                fe.hold = 654.45
            if fe.id == 3954:
                fe.hold = 704.32
            if fe.id == 3957:
                fe.hold = 753.58
            elif fe.id == 3966:
                fe.hold = 401.61

            # todo 新能源汽车
            if fe.id == 3943:
                fe.hold = 183.18
            if fe.id == 3955:
                fe.hold = 414.13
            elif fe.id == 3990:
                fe.hold = 451.47

            # todo 医疗
            if fe.id == 3932:
                fe.hold = 143.72
            if fe.id == 3931:
                fe.hold = 143.72
            if fe.id == 3931:
                fe.hold = 143.72
            if fe.id == 3947:
                fe.hold = 153.28
            if fe.id == 3615:
                fe.hold = 234.74
            elif fe.id == 3970:
                fe.hold = 175.01

            fe.save(update_fields=['hold_rate', 'hold', ])

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
        headers = ['ID', '交易日期', '基金名称', '确认份额', '确认金额', '持有市值', ]
        for header in headers:
            table.add_column(header, justify="left", no_wrap=True)

        tabulate_table = []
        for fund_category in dict(Fund.FUND_CATEGORY).keys():
            for fund_expense in FundExpense.objects.filter(fund__category=fund_category, expense_type='buy',
                                                           need_buy_again=False).exclude(
                expense=0).order_by('-hold_rate')[:9]:
                last_fundvalue = FundValue.objects.filter(fund=fund_expense.fund).order_by('deal_at').last()
                value = round(fund_expense.hold * last_fundvalue.value, 2)
                hold_rate_persent = f"{(((value - fund_expense.expense) / fund_expense.expense) * 100):0.02f}%"
                table.add_row(
                    f'{fund_expense.id}',
                    f'{fund_expense.deal_at}',
                    f'{fund_expense.fund.name}',
                    f'{fund_expense.hold}',
                    f'{fund_expense.expense}',
                    f'{hold_rate_persent}',
                )
                tabulate_table.append([
                    f'{fund_expense.id}',
                    f'{fund_expense.deal_at}',
                    f'{fund_expense.fund.name}',
                    f'{fund_expense.hold}',
                    f'{fund_expense.expense}',
                    f'{hold_rate_persent}',
                ])
            table.add_row(
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
        requests.post('https://open.feishu.cn/open-apis/bot/v2/hook/f815d87c-433d-47dc-8377-d61c18f3e231', json=payload, timeout=5, )
