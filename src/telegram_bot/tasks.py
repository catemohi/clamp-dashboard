from celery import shared_task
from logging import getLogger
from typing import Mapping, Sequence

from .services import push_to_telegram


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
