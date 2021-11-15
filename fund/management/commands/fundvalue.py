import datetime

import httpx
from django.core.management.base import BaseCommand

from fund.models import Fund, FundValue, FundExpense


class Command(BaseCommand):
    def handle(self, *_, **options):

        data = {
            '诺安成长混合': {
                'N年年化': [229, 3 * 12 * 30],
                '交易流水': [
                    ('2021-08-06', 10, 4.09), ('2021-08-10', 990.23, 421.28), ('2021-08-28', 139.09, 62.59),
                    ('2021-09-16', 479.68, 234.32),
                    ('2021-09-29', 482.49, 233.08), ('2021-10-11', 520.49, 255.76), ('2021-10-12', 539.0, 273.89),
                    ('2021-10-18', 434.94, 215.74),
                    ('2021-10-20', 79.79, 39.78),
                    ('2021-10-27', 586.66, 244.01 + 42.29),
                ],
                '代码': '320007',
            },
        }

        FundExpense.objects.filter(fund=Fund.objects.get(name='诺安成长混合')).delete()
        for d in data['诺安成长混合']['交易流水']:
            deal_at = d[0]
            fund = Fund.objects.get(name='诺安成长混合')
            expense = d[1]
            print(d, ' xxxxx')
            fund_value = FundValue.objects.get(fund=fund, deal_at=deal_at)
            hold = FundExpense.get_hold(fund_value=fund_value.value, expense=expense)
            FundExpense.objects.create(deal_at=deal_at, fund=fund, expense=expense, hold=hold)

        return
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        end_date = datetime.datetime.now()
        start_date = (end_date - datetime.timedelta(days=30 * 5)).strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        for fund in Fund.objects.all():
            url = f'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode={fund.code}&startdate={start_date}&enddate={end_date}'
            r = httpx.get(url=url, headers=headers, timeout=40)
            content = str(r.content)
            content_split_list = content.split('<tr>')

            for content_split in content_split_list:
                # if '2019-' not in content_split or '2020-' not in content_split or '2021-' not in content_split or '2022-' not in content_split:
                #     content
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
