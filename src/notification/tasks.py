from celery import shared_task
from logging import getLogger

from .services import create_default_burned_notification_setting
from .services import create_default_returned_notification_setting

LOGGER = getLogger(__name__)


@shared_task()
def create_burned_notification_models():
    """Функция создания моделей условий создания уведомлений о привышении
    лимита времени отработки обращения
    """
    create_default_burned_notification_setting()


@shared_task()
def create_returned_notification_models():
    """Функция создания моделей условий создания уведомлений о возвращении
    обращения на шаг ТП
    """
    create_default_returned_notification_setting()
