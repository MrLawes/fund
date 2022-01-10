import datetime
import json

import httpx
from django.core.management.base import BaseCommand
from tabulate import tabulate

from fund.models import Fund, FundValue, FundExpense


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
            # print(f'{fund}: {newest_url=}; {content=}')
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
            print(f'{fund.name}: {url=}')
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

        希望持有市值配置 = {
            # "[军工]鹏华空天军工指数(LOF)C": 1000,
            # "[医疗]中欧医疗C": 1000,
            # "[医疗]工银前沿医疗股票C": 1000,
            # "[半导体]华夏国证半导体芯片ETF联接C": 1000,
            # "[半导体]国泰半导体C": 1000,
            # "[半导体]银河创新成长混合C": 1000,
            # "[新能源]工银瑞信新能源汽车主题混合C": 1000,
            # "[白酒]招商中证白酒指数C": 1000,

            "[半导体]诺安成长混合": 4000,
            "[半导体]银河创新成长混合A": 1000,
            "[医疗]中欧医疗A": 11000,
            "[白酒]招商中证白酒指数(LOF)A": 3500,
            "[军工]易方达国防军工混合": 1000,
            "[新能源]农银工业4.0混合": 1000,
        }
        tabular_data = []

        for fund in Fund.objects.filter(name__in=list(希望持有市值配置.keys())):
            待回购市值 = list(
                FundExpense.objects.filter(
                    fund=fund, expense_type='sale', is_buy_again=False
                ).values_list('expense', flat=True))
            待回购市值 = sum(待回购市值)
            fund_value = FundValue.objects.filter(fund=fund, ).order_by('deal_at').last()
            hold = sum(FundExpense.objects.filter(fund=fund, expense_type='buy').values_list('hold', flat=True))
            建议购买 = (希望持有市值配置[fund.name] - 待回购市值) - (fund_value.value * hold)
            if 建议购买 < 0:
                建议购买 = 0
            tabular_data.append(
                [f"{(fund_value.value * hold):0.02f}", f"{(希望持有市值配置[fund.name] - 待回购市值):0.02f}",
                 建议购买, fund.name])
        # 输出结果
        headers = ['持有市值', '  目标市值', '   建议购买（元）', '      基金名称', ]
        print(tabulate(tabular_data=tabular_data, headers=headers, numalign='left'))
