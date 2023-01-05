from json import dumps
from typing import Mapping, Literal, Any
from enum import Enum
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import NotificationMessage


CHANNEL_LAYER = get_channel_layer()


class IssueNotification(Enum):
    """Класс типов уведомлений
    """

    NEW = 1
    CHANGED = 2
    CLOSED = 3
    BURNED = 4
    RETURNED = 5


def create_update_message(issue: Mapping, changed: Mapping) -> str:
    """Функция для генерации текста уведомления о изменении.
    Т.к приоретет уведомлений не одинаков. Возвратиться самое преоритетное
    уведомление.

    Args:
        issue (Mapping): обращение
        changed (Mapping): извенения

    Returns:
        str: текст уведомления
    """
    emodji = (lambda issue: '❤️' if issue['vip_contragent'] else '')(issue)
    message = ''
    if changed.get('return_to_work_time', False):
        message = (f'{emodji} Время решения обращения номер '
                   f'{issue.get("number")} изменено на '
                   f'{issue.get("return_to_work_time")}')

    if changed.get('step', False):
        message = (f'{emodji} Обращение номер {issue.get("number")} '
                   f'переведено на шаг {issue.get("step")}')

    if changed.get('responsible', False):
        message = (f'{emodji} Ответственным за обращение номер '
                   f'{issue.get("number")} назначен(а) '
                   f'{issue.get("responsible")} шаг {issue.get("step")}')
    return message


def send_notification(issue: Mapping, *args, **kwargs):
    """Уведомление о новом обращении.
    """

    time = datetime.strftime(datetime.now(), '%d.%m.%y %H:%M:%S')

    if kwargs.get('type') == IssueNotification.CHANGED:
        message = create_update_message(issue, kwargs['changed'])
        result = (
            "clamp",
            {"type": "notification", "subtype": "updated", "issue": issue, "text": message, "time": time},
            )

    elif kwargs.get('type') == IssueNotification.NEW:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        emodji = (lambda issue: '❤️' if issue['vip_contragent']
                  else '')(issue)
        message = (f'{emodji} На {group} появилось новое обращение номер '
                   f'{issue.get("number")}')
        result = (
            "clamp",
            {"type": "notification", "subtype": "new", "issue": issue, "text": message, "time": time},
            )

    elif kwargs.get('type') == IssueNotification.CLOSED:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        emodji = (lambda issue: '❤️' if issue['vip_contragent']
                  else '')(issue)
        message = (f'{emodji} На {group} закрыто или переведено с шага '
                   f'обращение номер {issue.get("number")}')
        result = (
            "clamp",
            {"type": "notification", "subtype": "closed", "issue": issue, "text": message,
             "time": time},
            )

    elif kwargs.get('type') == IssueNotification.RETURNED:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'🧨 ПРЕДУПРЕЖДЕНИЕ! В {issue.get("return_to_work_time")} '
                   f'на {group} c отложенного шага {issue.get("step")}'
                   f'вернется обращение номер {issue.get("number")}')
        result = (
            "clamp",
            {"type": "notification", "subtype": "returned", "issue": issue, "text": message,
             "time": time})

    elif kwargs.get('type') == IssueNotification.BURNED:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'🧨 ПРЕДУПРЕЖДЕНИЕ! Обращение номер {issue.get("number")} '
                   f'находится на {issue.get("responsible")} '
                   f'{issue.get("step_time") // 60} минут!')
        result = (
            "clamp",
            {"type": "notification", "subtype": "burned", "issue": issue, "text": message,
             "time": time})

    NotificationMessage(text=result[1]["text"],
                        datetime=result[1]["time"],
                        issue=result[1]["issue"]).save()
    async_to_sync(CHANNEL_LAYER.group_send)(*result)


def get_notify(*args, slice: int = 0, **kwargs) -> list[dict]:
    """
    Функция для получения сохраненных в БД уведомлений.
    Можно использовать slice для извлечения определенного количества данных
    По умолчанию выдаст все сохраненные строки.

    Args:
        slice (int): Срез. По умолчанию 0.

    Returns:
        str: JSON строка уведомлений.
    """
    notify = NotificationMessage.objects.order_by('datetime').reverse()[:50]
    return notify


def send_report(sended_data: dict[Literal['dates', 'dashboard_data'], Any]):
    """
    """
    result = ("clamp", {"type": "reports", **sended_data})
    async_to_sync(CHANNEL_LAYER.group_send)(*result)


def send_count(sended_data: dict[Literal['first_line', 'vip_line'], Any]):
    """
    """
    result = ("clamp", {"type": "count", **sended_data})
    async_to_sync(CHANNEL_LAYER.group_send)(*result)
