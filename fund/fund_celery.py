import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('fund_celery')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Shanghai'
app.conf.beat_schedule = {
    'refresh_fund_1': {
        'task': 'fund.tasks.refresh_fund',
        'schedule': crontab(hour=14, minute=30),
        'args': (),
    },
    'refresh_fund_2': {
        'task': 'fund.tasks.refresh_fund',
        'schedule': crontab(hour=12, minute=0),
        'args': (),
    },
    'refresh_fund_3': {
        'task': 'fund.tasks.refresh_fund',
        'schedule': crontab(hour=14, minute=55),
        'args': (),
    },
}

default_exchange = Exchange('fund_celery', type='direct')
app.conf.task_queues = (
    Queue('fund_celery', default_exchange, routing_key='fund_celery'),
)
app.conf.task_default_queue = 'fund_celery'
app.conf.task_default_exchange = 'fund_celery'
app.conf.task_default_routing_key = 'fund_celery'
