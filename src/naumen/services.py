from calendar import monthrange
from datetime import date, datetime, timedelta
from json import loads
from logging import getLogger
from typing import Callable, Mapping, Sequence, Tuple, Union, List, Literal

from django.conf import settings
from django.core import serializers
from django.db import models
from django.utils.timezone import make_aware
from django.db.models import QuerySet


from naumen_api.naumen_api.config.config import CONFIG
from naumen_api.naumen_api.naumen_api import Client

from notification.models import StepNotificationSetting
from notification.models import RetrunToWorkNotificationSetting
from notification.services import send_notification, IssueNotification

from pytz import timezone

from .exceptions import NaumenBadRequestError, NaumenConnectionError
from .exceptions import NaumenServiceError
from .models import FlrReport, Issue
from .models import MeanTimeToResponseReport, ServiceLevelReport


NAUMEN_CLIENT = None
LOGGER = getLogger(__name__)


def parse_naumen_api_responce(responce: str) -> Sequence:

    """Функция для парсинга ответа naumen_api.

    Args:
        responce (str): ответ от naumen_api

    Returns:
        Sequence: колекция ответа
    """

    responce = loads(responce)
    status_code = responce.get('status_code')
    status_message = responce.get('status_message')
    description = responce.get('description')
    content = responce.get('content')
    return status_code, status_message, description, content


def get_connect_to_naumen() -> Client:

    """Создание сессии с CRM, для взаимодействия.

    Returns:
        Client: клиент взаимодействия.
    """
    CONFIG.config_path = 'config.json'
    CONFIG.load_config()
    client = Client()
    responce = client.connect(username=settings.NAUMEN_LOGIN,
                              password=settings.NAUMEN_PASSWORD,
                              domain='CORP.ERTELECOM.LOC')

    try:
        response_analysis(responce)
        return client

    except (NaumenConnectionError, NaumenBadRequestError):
        return None


def client_validation(func: Callable) -> Callable:

    """Валидация клиента naumen.

    Args:
        func (Callable) : декорируемая функция
    """

    def wrapper(*args, **kwargs):

        global NAUMEN_CLIENT

        if not isinstance(NAUMEN_CLIENT, Client):
            NAUMEN_CLIENT = get_connect_to_naumen()
            # Попытка переподнять соединение
            if not isinstance(NAUMEN_CLIENT, Client):
                raise NaumenConnectionError('Failed to connect to CRM NAUMEN')
        return func(*args, **kwargs)

    return wrapper


def add_months(start_date: date, months: int) -> date:

    """Функция для прибавления месяцев.

    Args:
        start_date (date): начальная дата.
        months (int): количество месяцев котррые необходимо прибавить.

    Returns:
        date: новая дата
    """

    month = start_date.month - 1 + months
    year = int(start_date.year + month / 12)
    month = month % 12 + 1
    day = min(start_date.day, monthrange(year, month)[1])
    return date(year, month, day)


def get_dates_for_report() -> Tuple[str, str]:

    """Получение дат для отчета. Первый день, нынешнего месяца
    и следующего.

    Returns:
        Tuple(str, str): Первый день, нынешнего месяц и следующего.
    """

    date_now = datetime.now()
    month, year = date_now.month, date_now.year
    start_date = date(year, month, 1)
    end_date = add_months(start_date, 1)
    return (start_date.strftime("%d.%m.%Y"), end_date.strftime("%d.%m.%Y"))


def response_analysis(responce: str) -> Sequence:

    """Анализ ответа от naumen.

    Args:
        responce (str): ответ от naumen

    Returns:
        Sequence: контент ответа
    """

    global NAUMEN_CLIENT

    status_code, status_message, description, content = \
        parse_naumen_api_responce(responce)

    message = f'{status_code} - {status_message}. {description}'

    if status_code == 200:
        return content

    if status_code == 400:
        raise NaumenBadRequestError(message)

    NAUMEN_CLIENT = None
    raise NaumenConnectionError(message)


@client_validation
def get_naumen_api_report(report_name: str, *args, **kwargs) -> Sequence:

    """Получение отчёта от naumen.

    Args:
        report_name (str): название отчета .
        *args: другие позиционнные аргементы

    Kwargs:
        **kwargs: именнованные аргементы.

    Returns:
        Sequence: контент ответа.
    """

    global NAUMEN_CLIENT

    start_date = kwargs.get('start_date', None)
    end_date = kwargs.get('end_date', None)
    deadline = kwargs.get('deadline', 15)
    is_vip = kwargs.get('is_vip', False)
    parse_issues_cards = kwargs.get('parse_issues_cards', False)
    parse_history = kwargs.get('parse_history', False)
    naumen_uuid = kwargs.get('naumen_uuid', None)

    if not all([start_date, end_date]):
        start_date, end_date = get_dates_for_report()

    reports = {
        'service_level': [
            NAUMEN_CLIENT.get_sl_report,
            [start_date, end_date, deadline],
            {},
        ],

        'mttr': [
            NAUMEN_CLIENT.get_mttr_report,
            [start_date, end_date],
            {},
        ],

        'flr': [
            NAUMEN_CLIENT.get_flr_report,
            [start_date, end_date],
            {},
        ],

        'issues': [
            NAUMEN_CLIENT.get_issues,
            [],
            {'is_vip': is_vip,
             'parse_issues_cards': parse_issues_cards,
             'parse_history': parse_history,
             },
        ],

        'issue_card': [
            NAUMEN_CLIENT.get_issue_card,
            [naumen_uuid],
            {},
        ],
    }

    report, report_args, report_kwargs = reports.get(report_name,
                                                     [False, [], {}])

    if not report:
        raise NaumenBadRequestError('Report name not found')

    responce = report(*report_args, **report_kwargs)
    return responce


def change_model_fields(model: models.Model, search_field: dict,
                        set_fields: dict, *args, **kwargs) -> models.Model:
    """
    Изменение полей модели.

    Args:
        model (models.Model): модель
        search_field (dict): поля по которому будет найдена модель
        set_fields (dict): поля которые требуется изменить.
    """
    if not kwargs.get('is_created', True):
        obj = model()

    else:
        queryset = model.objects.filter(**search_field)

        if len(queryset) > 1:
            raise NaumenServiceError(f'По полю {search_field},'
                                     f' найдено {len(queryset)}.'
                                     ' Уточните данные.')
        if not queryset:
            raise NaumenServiceError(f'По полю {search_field},'
                                     f'не найдено обьектов.'
                                     ' Уточните данные.')

        obj = queryset[0]

    for field, value in set_fields.items():
        setattr(obj, field, value)

    obj.save()
    return obj


def create_or_update_service_level_report_model(date: date, group: str,
                                                attributes: dict) -> None:

    """Создание или обновление обьекта отчета SL.

    Args:
        date (datetime): дата отчета.
        group (str): группа отчета.
        attributes (dict): атрибуты для создания/обновления модели.
    """

    try:
        obj = ServiceLevelReport.objects.get(date=date, name_group=group)
    except ServiceLevelReport.DoesNotExist:
        obj = ServiceLevelReport()
    except:
        raise NaumenServiceError

    obj.date = date
    obj.name_group = group
    obj.total_number_trouble_ticket = int(attributes['total_issues'])
    obj.number_primary_trouble_tickets = \
        int(attributes['total_primary_issues'])
    obj.number_of_trouble_ticket_taken_before_deadline = \
        int(attributes['num_issues_before_deadline'])
    obj.number_of_trouble_ticket_taken_after_deadline = \
        int(attributes['num_issues_after_deadline'])
    obj.service_level = float(attributes['service_level'])
    obj.save()


def create_or_update_group_mttr_report_model(report: dict) -> None:

    """Создание или обновление обьекта отчета MTTR.

    Args:
        report (dict): словарь параметров отчета.
    """

    try:
        obj = MeanTimeToResponseReport.objects.get(date=report['date'])
    except MeanTimeToResponseReport.DoesNotExist:
        obj = MeanTimeToResponseReport()
    except:
        raise NaumenServiceError

    obj.date = report['date']
    obj.total_number_trouble_ticket = report['total_issues']
    obj.average_mttr = timedelta(
        minutes=round(float(report['average_mttr']), 0))
    obj.average_mttr_tech_support = timedelta(
        minutes=round(float(report['average_mttr_tech_support']), 0))
    obj.save()


def create_or_update_group_flr_report_model(report: dict) -> None:

    """Создание или обновление обьекта отчета FLR.

    Args:
        report (dict): словарь параметров отчета.
    """

    try:
        obj = FlrReport.objects.get(date=report['date'])
    except FlrReport.DoesNotExist:
        obj = FlrReport()
    except:
        raise NaumenServiceError

    obj.date = report['date']
    obj.flr_level = float(report['flr_level'])
    obj.number_trouble_ticket_closed_independently = \
        int(report['num_issues_closed_independently'])
    obj.number_primary_trouble_tickets = \
        int(report['total_primary_issues'])
    obj.save()


def create_or_update_issue_model(issue: dict) -> None:

    """Создание или обновление обьекта обращения.

    Args:
        issue (dict): словарь параметров обращения.
    """
    issue = {**issue,
             'url_issue': settings.NAUMEN_URL['open2'] +
             '?uuid=' + issue.get('uuid'),
             'url_contragent': settings.NAUMEN_URL['open2'] +
             '?uuid=' + issue.get('uuid_contragent'),
             'url_service': settings.NAUMEN_URL['open2'] +
             '?uuid=' + issue.get('uuid_service'),
             }

    try:
        obj = Issue.objects.get(uuid=issue['uuid'])
        status, changed_dict = checking_issues_changes(obj, issue)
        if obj.alarm_deadline and status:
            obj.alarm_deadline = False
            obj.save()
        if obj.alarm_return_to_work and status:
            obj.alarm_return_to_work = False
            obj.save()

        if status:
            send_notification(
                issue,
                **{"type": IssueNotification.CHANGED, "changed": changed_dict})

        change_model_fields(Issue, {'uuid': issue.get('uuid')},
                            _converter_timestring_to_timeobj_for_obj(issue))

    except Issue.DoesNotExist:
        send_notification(issue, **{"type": IssueNotification.NEW})
        change_model_fields(Issue, {'uuid': issue.get('uuid')},
                            {"alarm_deadline": False,
                             "alarm_return_to_work": False,
                             **_converter_timestring_to_timeobj_for_obj(
                                 issue)},
                            is_created=False)

    except:
        raise NaumenServiceError


def delete_issue_model(issue: dict) -> bool:

    """Удаление обьекта обращения.

    Args:
        uuid (str): уникальный идентификатор обращения

    Returns:
        bool: результат попытки удаления обьекта.
    """
    try:
        obj = Issue.objects.get(uuid=issue.get('uuid'))
    except Issue.DoesNotExist:
        raise NaumenServiceError('Не удалось удалить обьект обращение с UUID: '
                                 '%s' % issue.get('uuid'))

    send_notification(issue, **{"type": IssueNotification.CLOSED})
    obj.delete()
    return True


def crud_service_level(*args, **kwargs) -> None:

    """Функция для синзронизации отчетов SL Naumen и db.

    Args:
        *args: позиционные аргументы, не используются.

    Kwargs:
        *kwargs: именнованные аргуметы, пробрасываются в naumen_api.

    """

    start_date = kwargs.get("start_date", '')
    end_date = kwargs.get("end_date", '')
    deadline = kwargs.get("deadline", 15)

    if not any([start_date, end_date]):
        start_date, end_date = get_dates_for_report()
        kwargs = {
            "start_date": start_date,
            "end_date": end_date,
            "deadline": deadline,
            }

    responce = get_naumen_api_report("service_level", **kwargs)
    content = response_analysis(responce)
    _ = datetime.strptime(start_date, "%d.%m.%Y")
    for day_report in content:
        for group_report in day_report:
            group = group_report.pop("group")
            report_date = date(_.year, _.month, int(group_report.pop("day")))
            try:
                create_or_update_service_level_report_model(report_date,
                                                            group,
                                                            group_report)
            except NaumenServiceError as err:
                LOGGER.exception(err)


def crud_mttr(*args, **kwargs) -> None:

    """Функция для синзронизации отчетов MTTR Naumen и db.

    Args:
        *args: позиционные аргументы, не используются.

    Kwargs:
        *kwargs: именнованные аргуметы, пробрасываются в naumen_api.

    """

    start_date = kwargs.get("start_date", '')
    end_date = kwargs.get("end_date", '')

    if not any([start_date, end_date]):
        start_date, end_date = get_dates_for_report()
        kwargs = {
            "start_date": start_date,
            "end_date": end_date,
            }

    responce = get_naumen_api_report("mttr", **kwargs)
    content = response_analysis(responce)
    _ = datetime.strptime(start_date, "%d.%m.%Y")

    for day_report in content:
        day_report['date'] = date(_.year, _.month, int(day_report.pop("day")))

        try:
            create_or_update_group_mttr_report_model(day_report)
        except NaumenServiceError as err:
            LOGGER.exception(err)


def crud_flr(*args, **kwargs) -> None:

    """Функция для синзронизации отчетов FLR Naumen и db.

    Args:
        *args: позиционные аргументы, не используются.

    Kwargs:
        *kwargs: именнованные аргуметы, пробрасываются в naumen_api.

    """
    start_date = kwargs.get("start_date", '')
    end_date = kwargs.get("end_date", '')

    if not any([start_date, end_date]):
        start_date, end_date = get_dates_for_report()
        kwargs = {
            "start_date": start_date,
            "end_date": end_date,
            }

    responce = get_naumen_api_report("flr", **kwargs)
    content = response_analysis(responce)
    _ = datetime.strptime(start_date, "%d.%m.%Y")

    for day_report in content:
        day_report["date"] = datetime.strptime(day_report["date"], "%d.%m.%Y")

        try:
            create_or_update_group_flr_report_model(day_report)
        except NaumenServiceError as err:
            LOGGER.exception(err)


def download_issues(*args, **kwargs) -> str:

    """Функция для загрузки тикетов из CRM Naumen.

    Args:
        *args: позиционные аргументы, не используются.

    Kwargs:
        *kwargs: именнованные аргуметы, пробрасываются в naumen_api.

    Returns:
        str: json строка с данными

    """
    responce = get_naumen_api_report("issues", **kwargs)
    content = response_analysis(responce)
    return content


def crud_issue(*args, **kwargs) -> None:

    """Создание обьекта обращения в базе данных
    Args:
        *args: позиционные аргументы, не используются.

    Kwargs:
        *kwargs: именнованные аргуметы, пробрасываются в naumen_api.

    """

    try:
        if kwargs.get('is_delete', False):
            delete_issue_model(kwargs.get("issue").get('uuid'))
        create_or_update_issue_model(kwargs.get("issue"))
    except NaumenServiceError as err:
        LOGGER.exception(err)


def _converter_timestring_to_timeobj_for_obj(obj: dict) -> dict:
    """Конвертация временные строки в обьекты datetime

    Args:
        obj(dict): обьект в котором необходимо преобразровать строчки

    Returns:
        dict
    """

    for key, value in obj.items():

        try:

            value = make_aware(datetime.strptime(value, '%d.%m.%Y %H:%M:%S'))
            obj[key] = value

        except (ValueError, TypeError):
            pass

    if 'step_time' in obj:
        obj['step_time'] = int(obj['step_time'])

    return obj


def get_json_for_model(obj: models.Model, *args, ordering=(),
                       slice=0, **kwargs):
    """Сериализация моделей в json.

    Args:
        obj (models.Model): модели которые необходимо сериализовать.

    Kwargs:
        **kwargs: передаются именнованные аргументы для фильтрации моделей.
    """

    if kwargs:
        qs = obj.objects.filter(**kwargs)
    elif ordering:
        qs = obj.objects.order_by(*ordering)
    else:
        qs = obj.objects.all()
    if slice:
        qs = qs[:slice]

    return serializers.serialize('json', qs)


def parse_issue_card(issue: Mapping, *args, **kwargs) -> Mapping:
    """Функция для парсинга карточек обращений и добавления параметров.

    Args:
        issue (Mapping): обращение для которого необходимо спарсить карточку

    Kwargs:
        is_repeated (bool): флаг для повторного запроса парсинга карточки

    Returns:
        issue (Mapping): обновленное обращение

    Raises:
        NaumenConnectionError: в случае двух неудач парсинга.
    """

    try:
        responce = get_naumen_api_report("issue_card",
                                         **{**kwargs,
                                            'naumen_uuid': issue['uuid']},
                                         )
        content = response_analysis(responce)[0]
    except (NaumenConnectionError):

        if kwargs.get('is_repeated', False):
            LOGGER.error(f'Issue: {issue["name"]} not parse. UUID:'
                         f' {issue["uuid"]}. Repeat error!')
            raise NaumenConnectionError

        LOGGER.error(f'Issue: {issue["name"]}'
                     f' not parse. UUID: {issue["uuid"]}')
        parse_issue_card(issue, is_repeated=True)

    [issue.update({key: value}) for key, value in content.items() if value]
    return issue


def get_issues_from_db(*args, **kwargs):
    """Функция для возврата обращений из базы данных
    """
    issues = [{'uuid': issue.get('pk'),
               **issue.get("fields")}
              for issue in loads(get_json_for_model(Issue, **kwargs))]
    return issues


def issues_list_synchronization(*args, **kwargs):
    """Функция сравнивает переданные обращения и обращение в базе.
    """

    kwargs.update({'vip_contragent': kwargs.pop('is_vip', False)})
    issues_from_naumen = kwargs.pop("issues")

    issues_from_db = get_issues_from_db(*args, **kwargs)

    uuids_from_naumen = set([issue['uuid'] for issue in issues_from_naumen])
    uuids_from_db = set([issue['uuid'] for issue in issues_from_db])

    deleted_uuids = (uuids_from_db - uuids_from_naumen)

    crud_issues = [issue for issue in issues_from_naumen
                   if issue['uuid'] not in deleted_uuids]

    deleted_issues = [issue for issue in issues_from_db
                      if issue['uuid'] in deleted_uuids]

    return (crud_issues, deleted_issues)


def checking_issues_changes(old_issue: Issue,
                            new_issue: Mapping) -> Tuple[bool, dict]:
    """Функиция для проверки изменений в обращении.

    Args:
        old_issues (Mapping): старое обращения.
        old_issues (Mapping): новое обращение.
    Returns:
        Tuple[bool, dict]: статус проверки, словарь изменений
    """
    changed_dict = {}
    step_is_changed = old_issue.step != new_issue["step"]
    responsible_is_changed = (old_issue.responsible
                              !=
                              new_issue["responsible"])

    old_return_to_work_time = old_issue.return_to_work_time\
        .astimezone(timezone(settings.TIME_ZONE))\
        .strftime('%d.%m.%Y %H:%M:%S')

    return_to_work_time_is_changed = (old_return_to_work_time
                                      !=
                                      new_issue["return_to_work_time"])

    issue_is_changed = any([responsible_is_changed,
                            step_is_changed,
                            return_to_work_time_is_changed])
    if issue_is_changed:
        changed_dict = {'responsible': responsible_is_changed,
                        'step': step_is_changed,
                        'return_to_work_time': return_to_work_time_is_changed}

    return issue_is_changed, changed_dict


def check_issue_return_timers(issue: Mapping, *args, **kwargs) -> None:
    """Проверка таймера возврата в работу.

    Args:
        issue (Issue): обращение которое необходимо проверить
    """

    issue_step = issue['step']
    try:
        timer = RetrunToWorkNotificationSetting.objects.get(step=issue_step)

    except RetrunToWorkNotificationSetting.MultipleObjectsReturned:
        LOGGER.error('Найдено более 1 настроки уведомления возврате'
                     f' для "{issue_step}".Пропуск обращения.')
        return

    except RetrunToWorkNotificationSetting.DoesNotExist:
        LOGGER.debug('Не найдено настроки уведомления возврате'
                     f' для "{issue_step}".Пропуск обращения.')
        return

    issue_return_to_work_time = datetime.strptime(
                                            issue['return_to_work_time'],
                                            '%Y-%m-%dT%H:%M:%SZ')
    issue_return_to_work_time = issue_return_to_work_time\
        .astimezone(timezone(settings.TIME_ZONE))

    issue['return_to_work_time'] = issue_return_to_work_time\
        .strftime('%d.%m.%Y, %H:%M:%S')
    print('Issue time: ', issue_return_to_work_time)
    print('NOW time: ', datetime.now().astimezone(timezone(settings.TIME_ZONE)))
    time_difference = (issue_return_to_work_time -
                       datetime.now().astimezone(timezone(settings.TIME_ZONE))
                       ).seconds
    print('TIME DIFFERENCE: ',time_difference),
    print('ALARM TIME: ', timer.alarm_time)
    pushing = 0 < time_difference < timer.alarm_time

    if pushing is True and not issue['alarm_return_to_work']:
        change_model_fields(Issue, {'uuid': issue.get('uuid')},
                            {"alarm_return_to_work": True})
        send_notification(issue, type=IssueNotification.RETURNED)


def check_issue_deadline(issue: Mapping, *args, **kwargs) -> None:
    """Проверка времени отработки на шаге и таймера возврата в работу.

    Args:
        issue (Issue): обращение которое необходимо проверить
    """

    issue_step = issue['step']
    try:
        deadline = StepNotificationSetting.objects.get(step=issue_step)

    except StepNotificationSetting.MultipleObjectsReturned:
        LOGGER.error('Найдено более 1 настроки уведомления времени отработки '
                     f'для "{issue_step}".Пропуск обращения.')
        return

    except StepNotificationSetting.DoesNotExist:
        LOGGER.debug('Не найдено настроки уведомления времени отработки '
                     f'для "{issue_step}".Пропуск обращения.')
        return

    time_difference = deadline.step_time - issue['step_time']
    pushing = deadline.alarm_time >= time_difference > 0

    if pushing is True and not issue['alarm_deadline']:
        change_model_fields(Issue, {'uuid': issue.get('uuid')},
                            {"alarm_deadline": True})
        send_notification(issue, type=IssueNotification.BURNED)


def get_report_to_period(
    model: Literal['sl', 'flr', 'mttr'], start_date: date, end_date: date,
        **filter_fields: Mapping) -> Union[QuerySet, List[models.Model]]:
    """
    Фунция для получения данных по отчетам за период из базы данных.

    Args:
        model (Literal['sl', 'flr', 'mttr']): литерал на модель отчета
        start_date (date): дата первого дня интересующего периода
        end_date (date): дата последнего дня интересующего периода
        **filter_fields (Mapping): дополнительные поля фильтрации

    Returns:
        Union[QuerySet, List[models.Model]]: коллекция дней
    """
    models_dict: Mapping[str, models.Model] = {
        'sl': ServiceLevelReport,
        'flr': FlrReport,
        'mttr': MeanTimeToResponseReport
    }
    chosen_model = models_dict[model]
    qs = chosen_model.objects.filter(date__gte=start_date, date__lt=end_date,
                                     **filter_fields)
    return qs
