from celery import shared_task
from logging import getLogger
from typing import Mapping, Sequence

from .services import create_default_burned_notification_setting
from .services import create_default_returned_notification_setting
from .services import remove_notification
from telegram_bot.services import push_to_telegram


LOGGER = getLogger(__name__)


@shared_task()
def remove_old_notification():
    """Функция создания моделей условий создания уведомлений о привышении
    лимита времени отработки обращения
    """
    remove_notification()


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


@shared_task()
def push_notification_to_telegram(notification: Mapping) -> Sequence:
    """Отправка уведомления в телеграмм

    Args:
        notification (Mapping): уведомление

    Returns:
        Sequence: статус отправки
    """
    result = push_to_telegram(notification)
    return result
