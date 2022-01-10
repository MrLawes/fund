import datetime
import json

import httpx
from django.core.management.base import BaseCommand
from tabulate import tabulate

from fund.models import Fund, FundValue


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
            print(f'{fund}: {newest_url=}; {content=}')
            # 更新昨天的数据
            defaults = {'value': content['dwjz'], 'rate': 0}

            # jzrq 有两种格式： 1：2021-12-03；2：21-12-03
            deal_at = content['jzrq']
            if len(deal_at.split('-')[0]) == 2:
                deal_at = '20' + deal_at
            FundValue.objects.update_or_create(fund=fund, deal_at=deal_at, defaults=defaults)
            # 更新今天的数据
            defaults = {'value': content['gsz'], 'rate': content['gszzl']}
            FundValue.objects.update_or_create(fund=fund, deal_at=content['gztime'][:10], defaults=defaults)

            newest_fund_value = FundValue.objects.filter(fund=fund).order_by('deal_at').last()
            if newest_fund_value:
                fund.newest_rate = newest_fund_value.rate
                fund.save()

            url = f'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode={fund.code}&startdate={start_date}&enddate={end_date}'
            # print(f'{fund.name}: {url=}')
            try:
                r = httpx.get(url=url, headers=headers, timeout=10)
            except:
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

        希望持有市值 = {
            "[军工]鹏华空天军工指数(LOF)C": 1000,
            "[医疗]中欧医疗C": 1000,
            "[医疗]工银前沿医疗股票C": 1000,
            "[半导体]华夏国证半导体芯片ETF联接C": 1000,
            "[半导体]国泰半导体C": 1000,
            "[半导体]银河创新成长混合C": 1000,
            "[新能源]工银瑞信新能源汽车主题混合C": 1000,
            "[白酒]招商中证白酒指数C": 1000,

            "[军工]易方达国防军工混合": 1000,
            "[医疗]中欧医疗A": 1000,
            "[半导体]诺安成长混合": 1000,
            "[半导体]银河创新成长混合A": 1000,
            "[新能源]农银工业4.0混合": 1000,
            "[白酒]招商中证白酒指数(LOF)A": 1000,
        }
        tabular_data = []

        for fund in Fund.objects.all().order_by('name'):
            tabular_data.append([1, 希望持有市值[fund.name], fund.name])
            #
            # fund_value = FundValue.objects.filter(fund=fund, ).order_by('deal_at').last()
            #
            # total_fund_value
            # 未回购市值 = 持有市值[fund.name] - xxx
            #
            # #     fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
            # #     if not fund_value:
            # #         return '0'
            # #     hope_value = 0
            # #     for fund_expense in FundExpense.objects.filter(fund=obj, expense_type='buy'):
            # #         hope_value += fund_expense.hope_value
            # #     if hold * fund_value.value > hope_value:
            # #         result = f"""<span style="color: red;">{(hold * fund_value.value):0.02f}</span>"""
            # #     else:
            # #         result = f"""<span style="color: green;">{(hold * fund_value.value):0.02f}</span>"""
            # #     return format_html(f"""{result}/{hope_value:0.02f}　　　　　""")
            # #
            # # value.short_description = '金额/止赢金额✌️'
            # #
            # #
            #
            # tabular_data.append([fund.name])
            #
            # # class FundExpense(models.Model):
            # #     fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name='基金名称', )
            # #     deal_at = models.DateField(verbose_name='交易日期', db_index=True, )
            # #     expense = models.FloatField(verbose_name='确认金额', default=0)
            # #     hold = models.FloatField(verbose_name='确认份额', default=0)
            # #     hold_rate = models.FloatField(verbose_name='持有收益率', default=0)
            # #     sale_using_date = models.DateField(verbose_name='可售恢复时间', default=None, null=True,
            # #                                        blank=True, )  # todo delete
            # #     expense_type = models.CharField(verbose_name='基金交易类型: buy: 购买；sale：出售', max_length=8, default='buy')
            # #     split_hold = models.FloatField(verbose_name='拆分份额', default=0)
            # #     sale_at = models.DateField(verbose_name='出售日期', default=None, null=True, blank=True, )
            # #     is_buy_again = models.BooleanField(verbose_name='是否已经回购', default=False)
            #
            # #     hold = sum(FundExpense.objects.filter(fund=obj, expense_type='buy').values_list('hold', flat=True))
            # #     fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
            # #     if not fund_value:
            # #         return '0'
            # #     hope_value = 0
            # #     for fund_expense in FundExpense.objects.filter(fund=obj, expense_type='buy'):
            # #         hope_value += fund_expense.hope_value
            # #     if hold * fund_value.value > hope_value:
            # #         result = f"""<span style="color: red;">{(hold * fund_value.value):0.02f}</span>"""
            # #     else:
            # #         result = f"""<span style="color: green;">{(hold * fund_value.value):0.02f}</span>"""
            # #     return format_html(f"""{result}/{hope_value:0.02f}　　　　　""")
            # #
            # # value.short_description = '金额/止赢金额✌️'
            # #
            # #
            # continue

        # 输出结果
        headers = ['持有市值', '希望持有市值', '             基金名称', ]
        print(tabulate(tabular_data=tabular_data, headers=headers, numalign='left'))
