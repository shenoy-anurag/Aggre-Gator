import os

from celery import Celery
from kombu import Exchange, Queue


def make_celery(app):
    celery_app = Celery(
        app,
        backend=os.environ.get('CELERY_RESULT_BACKEND'),
        broker=os.environ.get('CELERY_BROKER_URL'),
        include=['web_scraper', 'web_scraper.celery_config.celery_tasks']
    )
    celery_app.conf.update(app.config)

    celery_app.conf['CELERY_TASK_QUEUES'] = (
        Queue('web_scraper', Exchange('web_scraper'), routing_key='web_scraper')
    )
    celery_app.conf['CELERY_DEFAULT_QUEUE'] = 'web_scraper'
    celery_app.conf['CELERY_DEFAULT_EXCHANGE_TYPE'] = 'direct'
    celery_app.conf['CELERY_DEFAULT_ROUTING_KEY'] = 'web_scraper'

    return celery_app
