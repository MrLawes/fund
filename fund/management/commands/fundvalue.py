import datetime

import httpx
from django.core.management.base import BaseCommand

from fund.models import Fund, FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):

        # data = {
        #
        #     '中欧医疗A': {
        #         'N年年化': [203, 3 * 12 * 30],
        #         '交易流水': [
        #             ('2021-08-05', 10, 0), ('2021-08-08', 490.29 + 500, 0), ('2021-08-11', -33.03, 0),
        #             ('2021-08-28', 249.5, 0),
        #             ('2021-09-29', 274.29, 0),
        #             ('2021-10-20', 473.17, 0), ('2021-10-14', 500.0, 0),
        #             ('2021-10-11', 511.6, 0), ('2021-10-18', 569.48, 0), ('2021-10-26', 543.6, 0),
        #             ('2021-10-27', 543.96, 1326.06),
        #             ('2021-11-01', 976.81, 298.18),
        #             ('2021-11-04', 500, 157.05),
        #             ('2021-11-08', 700, 224.74,),
        #         ],
        #         '代码': '003095',
        #         '恒定市值区间': [3.0640, 4.3100 - (4.3100 - 3.0640) * 0.261],
        #     },
        # }
        #
        # FundExpense.objects.filter(fund=Fund.objects.get(name='中欧医疗A')).delete()
        # for d in data['中欧医疗A']['交易流水']:
        #     deal_at = d[0]
        #     fund = Fund.objects.get(name='中欧医疗A')
        #     expense = d[1]
        #     print(d, ' xxxxx')
        #     fund_value = FundValue.objects.get(fund=fund, deal_at=deal_at)
        #     hold = FundExpense.get_hold(fund_value=fund_value.value, expense=expense)
        #     FundExpense.objects.create(deal_at=deal_at, fund=fund, expense=expense, hold=hold)

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
