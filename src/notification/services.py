from typing import Mapping, Literal, Union, Any
from enum import Enum
from datetime import datetime
from json import dumps

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers

from .models import NotificationMessage, StepNotificationSetting
from .models import RetrunToWorkNotificationSetting
from telegram_bot.tasks import push_notification_to_telegram


CHANNEL_LAYER = get_channel_layer()


class IssueNotification(Enum):
    """Класс типов уведомлений
    """

    NEW = 1
    CHANGED = 2
    CLOSED = 3
    BURNED = 4
    RETURNED = 5
    BACK_TO_WORK = 6


def create_update_message(issue: Mapping, changed: Mapping,
                          back_to_work: bool = False) -> str:
    """Функция для генерации текста уведомления о изменении.
    Т.к приоретет уведомлений не одинаков. Возвратиться самое преоритетное
    уведомление.

    Args:
        issue (Mapping): обращение
        changed (Mapping): извенения
        back_to_work(bool): обращение вернулось в работу

    Returns:
        str: текст уведомления
    """
    message = ''
    if back_to_work:
        group = (lambda issue: 'VIP линию' if issue['vip_contragent']
                 else 'WESTCALL линию')(issue)
        message = (f'Обращение номер {issue.get("number")} '
                   f'вернулось в работу на {group}')
        return message

    if changed.get('return_to_work_time', False):
        message = (f'Время решения обращения номер '
                   f'{issue.get("number")} изменено на '
                   f'{issue.get("return_to_work_time")}')

    if changed.get('step', False):
        message = (f'Обращение номер {issue.get("number")} '
                   f'переведено на шаг {issue.get("step")}')

    if changed.get('responsible', False):
        message = (f'Ответственным за обращение номер '
                   f'{issue.get("number")} назначен(а) '
                   f'{issue.get("responsible")} шаг {issue.get("step")}')
    return message


def send_notification(issue: Mapping, *args, **kwargs):
    """Уведомление о новом обращении.
    """

    time = datetime.now()
    if kwargs.get('type') == IssueNotification.BACK_TO_WORK:
        message = create_update_message(issue, kwargs['changed'], True)
        result = (
            "clamp",
            {"type": "notification", "subtype": "back_to_work", "issue": issue,
             "text": message, "time": time},
            )
        push_notification_to_telegram.delay(result[1])

    elif kwargs.get('type') == IssueNotification.CHANGED:
        message = create_update_message(issue, kwargs['changed'])
        result = (
            "clamp",
            {"type": "notification", "subtype": "updated", "issue": issue,
             "text": message, "time": time},
            )

    elif kwargs.get('type') == IssueNotification.NEW:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'На {group} появилось новое обращение номер '
                   f'{issue.get("number")}')
        result = (
            "clamp",
            {"type": "notification", "subtype": "new", "issue": issue,
             "text": message, "time": time},
            )
        push_notification_to_telegram.delay(result[1])

    elif kwargs.get('type') == IssueNotification.CLOSED:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'На {group} закрыто или переведено с шага '
                   f'обращение номер {issue.get("number")}')
        result = (
            "clamp",
            {"type": "notification", "subtype": "closed", "issue": issue,
             "text": message, "time": time},
            )

    elif kwargs.get('type') == IssueNotification.RETURNED:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'WESTCALL линии')(issue)
        message = (f'{issue.get("return_to_work_time")} '
                   f'на {group} c отложенного шага {issue.get("step")} '
                   f'вернется обращение номер {issue.get("number")}')
        result = (
            "clamp",
            {"type": "notification", "subtype": "returned", "issue": issue,
             "text": message, "time": time})
        push_notification_to_telegram.delay(result[1])

    elif kwargs.get('type') == IssueNotification.BURNED:
        group = (lambda issue: 'VIP линии' if issue['vip_contragent']
                 else 'первой линии')(issue)
        message = (f'ПРЕДУПРЕЖДЕНИЕ! Обращение номер {issue.get("number")} '
                   f'находится на {issue.get("responsible")} '
                   f'{issue.get("step_time") // 60} минут!')
        result = (
            "clamp",
            {"type": "notification", "subtype": "burned", "issue": issue,
             "text": message, "time": time})
        push_notification_to_telegram.delay(result[1])

    NotificationMessage(text=result[1]["text"],
                        time=result[1]["time"],
                        subtype=result[1]["subtype"],
                        issue=dumps(result[1]["issue"])).save()

    result[1]["time"] = result[1]["time"].isoformat()
    async_to_sync(CHANNEL_LAYER.group_send)(*result)


def get_notification(*args, json_type: bool = False,
                     slice: int = 50, **kwargs) -> Union[list[dict], str]:
    """
    Функция для получения сохраненных в БД уведомлений.
    Можно использовать slice для извлечения определенного количества данных
    По умолчанию выдаст все сохраненные строки.

    Args:
        json_type (bool): Вывести как json строку False
        slice (int): Срез. По умолчанию 50.

    Returns:
        Union[list[dict], str]: JSON строка уведомлений или список.
    """
    notifications = NotificationMessage.objects.order_by('-time')[:slice]
    if json_type:
        return serializers.serialize('json', notifications)
    return notifications


def remove_notification(*args, **kwargs) -> None:
    """
    Функция для удаления устаревших уведомлений из БД .
    """
    NotificationMessage.objects.filter(time__lt=datetime.now()).delete()


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


def _get_or_create_notification_model(
    notification_model: Union[
        StepNotificationSetting, RetrunToWorkNotificationSetting],
        model_kwarg: Mapping = {}) -> None:
    """
    Функция для создания обьектов настроек уведомлений.

    Args:
        model_kwarg (Mapping, optional): именнованные аргументы модели.
        По умолчанию {}.
    """
    obj, created = notification_model.objects.get_or_create(**model_kwarg)


def create_default_burned_notification_setting():
    """
    Функция создания моделей настроек уведомлений о лимитах обработки
    """
    default_settings = (
        {'name': 'Уведомление о лимите обработки на группе ТП',
         'step': 'передано в работу (напр тех под В2В)',
         'step_time': 900,
         'alarm_time': 300},
        {'name': 'Уведомление о лимите обработки на сотруднике',
         'step': 'принято в работу',
         'step_time': 1800,
         'alarm_time': 300},
        {'name': 'Уведомление о лимите обработки на сотруднике 2',
         'step': 'принято в обработку',
         'step_time': 1800,
         'alarm_time': 300},
    )
    [_get_or_create_notification_model(StepNotificationSetting, setting)
     for setting in default_settings]


def create_default_returned_notification_setting():
    """
    Функция создания моделей настроек уведомлений о возврате в работу
    """
    default_settings = (
        {'name': 'Уведомление о возврате переадресации(снятие)',
         'step': 'Запланирована дата обработки (снятие переадр)',
         'alarm_time': 300},
        {'name': 'Уведомление о возврате переадресации(установка)',
         'step': 'Запланирована дата обработки (установка переадр)',
         'alarm_time': 300},
        {'name': 'Уведомление о возврате с шага обратной связи',
         'step': 'ожидание обратной связи от клиента',
         'alarm_time': 300},
        {'name': 'Уведомление о возврате с шага запланирована дата обработки',
         'step': 'Запланирована дата обработки',
         'alarm_time': 300},
    )
    [_get_or_create_notification_model(
     RetrunToWorkNotificationSetting, setting) for setting in default_settings]


def get_burned_notification_setting():
    """Функция для получения настроек уведомлений о лимитах обработки
    """
    settings = [entry for entry in StepNotificationSetting.objects.values()]
    return dumps(settings)


def get_returned_notification_setting():
    """Функция для получения настроек уведомлений о лимитах обработки
    """
    settings = [entry for entry in RetrunToWorkNotificationSetting.objects.values()]
    return dumps(settings)


def get_burned_steps():
    """Функция для получения шагов работы
    """
    steps = [entry.step for entry in StepNotificationSetting.objects.all()]
    return steps
