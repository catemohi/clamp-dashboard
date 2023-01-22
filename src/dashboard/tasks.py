from celery import shared_task

from logging import getLogger

from .services import get_day_dates_and_data, json_encoding
from .services import issues_on_group
from notification.services import send_report, send_count

LOGGER = getLogger(__name__)


@shared_task(ignore_result=True)
def front_params_update():
    updated_params = get_day_dates_and_data()
    updated_params['dashboard_data'] = json_encoding(
        updated_params['dashboard_data'])
    updated_params['dates'] = json_encoding(updated_params['dates'])
    send_report(updated_params)
    return True


@shared_task(ignore_result=True)
def front_issues_count():
    updated_params = issues_on_group()
    send_count(updated_params)
    return True
