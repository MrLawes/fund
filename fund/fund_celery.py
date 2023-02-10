import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('lls_saas_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Shanghai'
app.conf.beat_schedule = {
    'redis_heart_beat': {  # redis 心跳
        'task': 'fund.tasks.test',
        'schedule': crontab(),
        'args': ()
    },

}

default_exchange = Exchange('fund_celery', type='direct')
app.conf.task_queues = (
    Queue('fund_celery', default_exchange, routing_key='fund_celery'),
)
app.conf.task_default_queue = 'fund_celery'
app.conf.task_default_exchange = 'fund_celery'
app.conf.task_default_routing_key = 'fund_celery'
