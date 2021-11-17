import datetime

import httpx
from django.core.management.base import BaseCommand

from fund.models import Fund, FundValue


class Command(BaseCommand):
    def handle(self, *_, **options):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        end_date = datetime.datetime.now()
        start_date = (end_date - datetime.timedelta(days=30 * 5)).strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        for fund in Fund.objects.all():

            newest_url = f'https://hq.sinajs.cn/etag.php?_=1637125090638&list=fu_{fund.code}'
            r = httpx.get(url=newest_url, headers=headers, timeout=40)
            content = str(r.content).split(',')
            date = content[-1].split('"')[0]
            value = float(content[2])
            last_fund_value = FundValue.objects.filter(fund=fund).exclude(deal_at=date).last().value
            if value > last_fund_value:
                rate = 1 - last_fund_value / value
            else:
                rate = value / last_fund_value - 1
            defaults = {'value': content[2], 'rate': round(rate * 100, 2)}

            FundValue.objects.update_or_create(fund=fund, deal_at=date, defaults=defaults)

            # newest_url = f"http://so.hexun.com/default.do?type=fund&key={fund.code}"
            # r = httpx.get(url=newest_url, headers=headers, timeout=40)
            # content = str(r.content)
            # content_split_list = content.split('<td>')
            # for content_split in content_split_list:
            #     if not ('class="green"' in content_split or 'class="red"' in content_split):
            #         continue
            #     else:
            #         newest_value = float(content_split.split('</span>')[0].split('>')[-1].replace('%', ''))
            #         defaults = {'value': newest_value, 'rate': 0}
            #         FundValue.objects.update_or_create(fund=fund, deal_at=datetime.datetime.now().date(),
            #                                            defaults=defaults)
            #         break

            url = f'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode={fund.code}&startdate={start_date}&enddate={end_date}'
            r = httpx.get(url=url, headers=headers, timeout=40)
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
