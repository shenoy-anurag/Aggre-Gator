import datetime
import logging
import time

from web_aggregator import celery_app

logger = logging.getLogger(__name__)


# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(datetime.timedelta(minutes=15), simple_task.s(), name='simple_task')


@celery_app.task(name='simple_task')
def simple_task():
    try:
        time.sleep(100)
    except Exception as e:
        logger.error(e)

# @celery_app.task(task="send_aws_sms")
# def send_aws_sms(message, phone_number):
#     response = sms_client.publish(PhoneNumber=phone_number, Message=message)
#     return response
