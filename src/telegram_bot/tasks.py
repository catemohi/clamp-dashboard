from celery import shared_task
from logging import getLogger
from typing import Mapping, Sequence

from telegram_bot import services


@shared_task()
def push_notification_to_telegram(notification: Mapping) -> Sequence:
    """Отправка уведомления в телеграмм

    Args:
        notification (Mapping): уведомление

    Returns:
        Sequence: статус отправки
    """
    result = services.push_to_telegram(notification)
    return result


@shared_task()
def push_day_report() -> None:
    """Отправка дневного отчета в телеграмм
    """
    services.day_report()
