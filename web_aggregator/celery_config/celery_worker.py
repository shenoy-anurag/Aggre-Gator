import os

from celery import Celery
from kombu import Exchange, Queue


def make_celery(app):
    celery_app = Celery(
        app,
        backend=os.environ.get('CELERY_RESULT_BACKEND'),
        broker=os.environ.get('CELERY_BROKER_URL'),
        include=['web_aggregator', 'web_aggregator.celery_config.celery_tasks']
    )
    celery_app.conf.update(app.config)

    celery_app.conf['CELERY_TASK_QUEUES'] = (
        Queue('web_aggregator', Exchange('web_aggregator'), routing_key='web_aggregator')
    )
    celery_app.conf['CELERY_DEFAULT_QUEUE'] = 'web_aggregator'
    celery_app.conf['CELERY_DEFAULT_EXCHANGE_TYPE'] = 'direct'
    celery_app.conf['CELERY_DEFAULT_ROUTING_KEY'] = 'web_aggregator'

    return celery_app
