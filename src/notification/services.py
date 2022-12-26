from json import dumps
from typing import Mapping
from enum import Enum
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import NotificationMessage

channel_layer = get_channel_layer()


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
    message = ''

    if changed.get('return_to_work_time', False):
        message = (f'Время решения обращения номер {issue.get("number")} '
                   f'изменено на {issue.get("return_to_work_time")}')

    if changed.get('step', False):
        message = (f'Обращение номер {issue.get("number")} переведено на шаг '
                   f'{issue.get("step")}')

    if changed.get('responsible', False):
        message = (f'Ответственным за обращение номер {issue.get("number")} '
                   f'назначен(а) {issue.get("responsible")}')
    return message


def notify_issue(issue: Mapping, *args, **kwargs):
    """Уведомление о новом обращении.
    """

    time = datetime.strftime(datetime.now(), '%d.%m.%y %H:%M:%S')

    if kwargs.get('type') == IssueNotification.CHANGED:
        message = create_update_message(issue, kwargs['changed'])
        result = (
            "issue_notifi",
            [{"type": "updated", "issue": issue, "text": message,
              "time": time}],
            )

    elif kwargs.get('type') == IssueNotification.NEW:
        group = (lambda issue: 'vip линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'На {group} появилось новое обращение номер '
                   f'{issue.get("number")}')
        result = (
            "issue_notifi",
            [{"type": "new", "issue": issue, "text": message, "time": time}],
            )

    elif kwargs.get('type') == IssueNotification.CLOSED:
        group = (lambda issue: 'vip линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'На {group} закрыто или переведено с шага обращение номер '
                   f'{issue.get("number")}')
        result = (
            "issue_notifi",
            [{"type": "closed", "issue": issue, "text": message,
              "time": time}],
            )

    elif kwargs.get('type') == IssueNotification.RETURNED:
        group = (lambda issue: 'vip линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'В {issue.get("return_to_work_time")} на {group} c'
                   f'отложенного шага вернется обращение {issue.get("step")}'
                   f'вернется обращение номер {issue.get("number")}')
        result = (
            "issue_notifi",
            [{"type": "returned", "issue": issue, "text": message,
             "time": time}])

    elif kwargs.get('type') == IssueNotification.BURNED:
        group = (lambda issue: 'vip линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'Внимание! Обращение номер {issue.get("number")}'
                   f'скоро привысит лимит времени отработки!')
        result = (
            "issue_notifi",
            [{"type": "burned", "issue": issue, "text": message,
             "time": time}])

    NotificationMessage(text=result[1][0]["text"],
                        datetime=result[1][0]["time"],
                        issue=result[1][0]["issue"]).save()
    async_to_sync(channel_layer.group_send)(*result)
    return result
