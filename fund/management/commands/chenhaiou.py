import datetime

import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *_, **options):
        url = f'http://127.0.0.1:11111/v4/fund_expense/docker_test/?user=1'
        for i in range(1, 100000):
            r = requests.get(url)
            print(f"[{datetime.datetime.now()}] {r.status_code=}; {r.content}")

        """
        docker build -t fund:v202202071648 .
        docker service create --update-delay 10s --update-parallelism 2 --name fund --replicas=5 --publish 11112:80 --stop-signal HUP fund:v202202071648
        docker service update --image fund:v202202071648 fund
        """

        # cd /Users/chenhaiou/Desktop/D/git/api; source venv/bin/activate; python manage_test.py chenhaiou
