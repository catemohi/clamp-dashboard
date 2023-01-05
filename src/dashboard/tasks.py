from celery import shared_task

from logging import getLogger

from .services import get_day_dates_and_data
from notification.services import send_report

LOGGER = getLogger(__name__)

@shared_task
def front_params_update():
    updated_params = get_day_dates_and_data()
    send_report(updated_params)
    return True