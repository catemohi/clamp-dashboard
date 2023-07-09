from datetime import date, datetime, time, timedelta
from typing import Literal, NamedTuple, Mapping
from typing import Union, List, Any

from django.db import models

from naumen import services as naumen_services


from .models import RatingSetting, NaumenSetting


class Dates(NamedTuple):
    """Класс для хранения коллекции дат.

    Хранит даты:
        - первое число месяца передоваемой даты
        - первое число следующего месяца
        - число начала недели
        - число конца недели
        - требуемая дата
        - следующий день
        - прошлый день

    """
    calends_this_month: date
    calends_next_month: date
    monday_this_week: date
    sunday_this_week: date
    chosen_date: date
    next_day: date
    before_day: date


class ReportServiceLevel(NamedTuple):
    """Класс для хранения отчета по SL для группы

    Хранит данные:
        - SL за требуемый день для группы
        - Количество поступивших обращений для группы
        - Количество первичных обращений для группы
        - Количество обращений принятых до крайнего срока для группы
        - Количество обращений принятых после крайнего срока для группы
        - SL за неделю для группы
        - SL за месяц для группы
    """
    mountly_sl: int
    weekly_sl: int
    dayly_sl: int
    num_issues: int
    num_primary_issues: int
    num_worked_before_deadline: int
    num_worked_after_deadline: int


class ReportMttr(NamedTuple):
    """Класс для хранения отчета по MTTR

    Хранит данные:
        - Общее количество обращений
        - Средний МТТР
        - Средний МТТР ТП за месяц
        - Средний МТТР ТП за неделю
        - Средний МТТР ТП за день
    """
    num_issues: int
    average_mttr: int
    mountly_average_mttr_tech_support: int
    weekly_average_mttr_tech_support: int
    average_mttr_tech_support: int


class ReportAht(NamedTuple):
    """Класс для хранения отчета по AHT

    Хранит данные:
        - Месячный AHT
        - Недельный AHT
        - Дневной AHT
        - Количество обращений за день
    """
    mountly_aht: int
    weekly_aht: int
    dayly_aht: int
    issues_received: int


class ReportFlr(NamedTuple):
    """Класс для хранения отчета по MTTR

    Хранит данные:
        - FLR за месяц (в %)
        - FLR за неделю (в %)
        - FLR за день (в %)
        - Количество обращений закрытых без других отделов
        - Количество первичных обращений
    """
    mountly_level: int
    weekly_level: int
    level: int
    num_issues_closed_independently: int
    num_primary_issues: int


class RatingAnalytics(NamedTuple):
    """Класс для хранения аналитики

    Хранит данные:
        - Нагрузка относительно нормы
        - Нагрузка относительно дня сравнения
    """
    rating_to_nominal: float
    rating_to_comparison: float


def json_encoding(obj: dict) -> str:
    """Кодирование словаря в JSON.

    Силами JSONEncoder, не получается верно конвертировать NamedTuple
    вложенный в словарь. Эта функция справляется с этой проблемой и
    конвретирует все вложенные NamedTuple d dict

    Args:
        obj (Mapping): обьект для конвретации.

    Returns:
        str: итоговый JSON
    """

    def _recursive_conversion(obj: dict) -> dict:
        if isinstance(obj, dict):
            for key, val in obj.items():
                obj[key] = _recursive_conversion(val)
        elif isinstance(obj, tuple) and hasattr(obj, '_asdict'):
            obj = obj._asdict()
            for key, val in obj.items():
                obj[key] = _recursive_conversion(val)
        elif isinstance(obj, (datetime, date, time)):
            obj = obj.isoformat()
        elif isinstance(obj, timedelta):
            obj = obj.seconds()
        return obj

    return _recursive_conversion(obj)


def convert_datestr_to_datetime_obj(datestring: str) -> datetime:
    """Функция конвертации строки даты в datetime обьект

    Args:
        datestring (str): строка даты

    Returns:
        datetime: обьект даты и времени
    """

    date = datetime.strptime(datestring, "%Y-%m-%d").date()
    datetime_obj = datetime.combine(date, time(13, 0))
    return datetime_obj


def _get_group_name(required_group: Literal['first_line_group_name',
                                            'vip_line_group_name',
                                            'general_group_name']) -> str:
    """
    Функция получения названия группы ТП

    Args:
        required_group (Literal[first_line_group_name,
                                vip_line_group_name, general_group_name]):
        какую группу необходимо получить.

    Returns:
        str: название группы или пустую строку
    """
    obj, created = NaumenSetting.objects.get_or_create(is_active=True)

    if required_group == 'first_line_group_name':
        return obj.first_group_name

    if required_group == 'vip_line_group_name':
        return obj.vip_group_name

    if required_group == 'general_group_name':
        return obj.general_group_name

    return ''


def _get_group_step_name() -> str:
    """
    Функция получения названия шага, когда обращение передано на группы ТП

    Returns:
        str: название шага группы
    """
    obj, created = NaumenSetting.objects.get_or_create(is_active=True)

    return obj.step_name_on_group


def get_date_collections(datestring: str) -> Dates:
    """Функция для возврата коллекции дат.

    На выходе мы получаем коллекцию дат:
        - первое число месяца передоваемой даты
        - первое число следующего месяца
        - число начала недели
        - число конца недели
        - требуемая дата
        - слудующий день от требуемой даты
        - предыдущий день от требуемой даты

    Args:
        datestring (str): строка даты от которой требуется выдать коллекцию

    Returns:
        Dates: коллекция дат.
    """
    chosen_datetime = convert_datestr_to_datetime_obj(datestring)
    chosen_date = chosen_datetime.date()

    first_day_month = date(chosen_date.year, chosen_date.month, 1)
    first_day_next_month = naumen_services.add_months(first_day_month, 1)

    _monday_days_passed = datetime.isoweekday(chosen_date) - 1
    monday_this_week = (chosen_datetime -
                        timedelta(days=_monday_days_passed)).date()

    _until_sunday = 7 - datetime.isoweekday(chosen_date)
    sunday_this_week = (chosen_datetime + timedelta(days=_until_sunday)).date()

    next_day = chosen_date + timedelta(days=1)
    before_day = chosen_date - timedelta(days=1)

    return Dates(first_day_month, first_day_next_month, monday_this_week,
                 sunday_this_week, chosen_date, next_day, before_day)


def z_parse_service_level(dates: Dates, chosen_group: str,
                         qs: Union[models.QuerySet,
                                   List[models.Model]]) -> ReportServiceLevel:
    """
    Функция для получения данных по отчёту SL для группы.

    На выходе мы получаем данные:
        - SL за требуемый день для группы
        - Количество поступивших обращений для группы
        - Количество первичных обращений для группы
        - Количество обращений принятых до крайнего срока для группы
        - Количество обращений принятых после крайнего срока для группы
        - SL за неделю для группы
        - SL за месяц для группы

    Args:
        dates (Dates): коллекция дат
        group (str): группа для которой необходима информация
        qs (Union[models.QuerySet, List[models.Model]]): данные из БД

    Returns:
        ReportServiceLevel: коллекция необходимых данных
    """
    if not qs.exists():
        return ReportServiceLevel(0, 0, 0, 0, 0, 0, 0)
    # Фильтруем данные для группы
    qs_for_month = qs.filter(name_group=chosen_group)
    qs_for_week = qs_for_month.filter(
        date__gte=dates.monday_this_week, date__lte=dates.sunday_this_week)
    qs_for_chosen_day = qs_for_month.filter(
        date=dates.chosen_date)

    # Высчитывание проценты SL
    monthly_tickets_before_deadline = sum(
        [report.number_of_trouble_ticket_taken_before_deadline
         for report in qs_for_month])
    monthly_total_ticket = sum(
        [report.total_number_trouble_ticket
         for report in qs_for_month])
    mountly_sl = 100.0

    if monthly_total_ticket:
        mountly_sl = (
            monthly_tickets_before_deadline / monthly_total_ticket) * 100

    mountly_sl = int(round(mountly_sl, 0))

    weekly_tickets_before_deadline = sum(
        [report.number_of_trouble_ticket_taken_before_deadline
         for report in qs_for_week])
    weekly_total_ticket = sum(
        [report.total_number_trouble_ticket
         for report in qs_for_week])
    weekly_sl = 100.0

    if weekly_total_ticket:
        weekly_sl = (
            weekly_tickets_before_deadline / weekly_total_ticket) * 100

    weekly_sl = int(round(weekly_sl, 0))

    dayly_sl = 100.0
    if qs_for_chosen_day.first().total_number_trouble_ticket:
        dayly_sl = qs_for_chosen_day.first().service_level
    dayly_sl = int(round(dayly_sl, 0))

    # Расскладываем доп. данные
    num_issues = qs_for_chosen_day.first().total_number_trouble_ticket
    num_primary_issues = qs_for_chosen_day.first()\
        .number_primary_trouble_tickets
    num_worked_before_deadline = qs_for_chosen_day.first()\
        .number_of_trouble_ticket_taken_before_deadline
    num_worked_after_deadline = qs_for_chosen_day.first()\
        .number_of_trouble_ticket_taken_after_deadline

    return ReportServiceLevel(mountly_sl, weekly_sl, dayly_sl, num_issues,
                              num_primary_issues, num_worked_before_deadline,
                              num_worked_after_deadline)


def _get_service_level(datestring: str) -> Mapping[Literal['sl'], Mapping[
        Literal['first_line', 'vip_line', 'general'], ReportServiceLevel]]:
    """Функция для получения данных по отчёту SL для групп.

    На выходе мы получаем данные:
        - SL за требуемый день по первой линии
        - Количество поступивших обращений на первую линию
        - Количество первичных обращений на первой линии
        - Количество обращений принятых до крайнего срока на первой линии
        - Количество обращений принятых после крайнего срока на первой линии
        - SL за требуемый день по вип линии
        - Количество поступивших обращений на вип линию
        - Количество первичных обращений на вип линии
        - Количество обращений принятых до крайнего срока на вип линии
        - Количество обращений принятых после крайнего срока на вип линии
        - Итоговый SL за требуемый день
        - Количество поступивших обращений итоговое
        - Количество первичных обращений итоговое
        - Количество обращений принятых до крайнего срока итоговое
        - Количество обращений принятых после крайнего срока итоговое
        - SL за неделю по первой линии
        - SL за неделю по вип линии
        - Итоговый SL за неделю
        - SL за месяц по первой линии
        - SL за месяц по вип линии
        - Итоговый SL за месяц

    Args:
        datestring (str): строка даты за которую требуется отчет.

    Returns:
        Mapping[Literal['sl'], Mapping[Literal['first_line', 'vip_line',
                                               'general'],
        ReportServiceLevel]]: словарь данных, с ключами по линиям ТП
    """
    today_date = datetime.now().date()
    # Операции над входящей строкой даты
    dates = get_date_collections(datestring)
    # Получение отчетов за месяц
    qs = naumen_services.get_report_to_period('sl', dates.calends_this_month,
                                              dates.calends_next_month)
    # Исключаем нулевые отчеты
    qs = qs.filter(date__lte=today_date)
    # Получение данных для первой линии.
    chosen_group = _get_group_name('first_line_group_name')
    first_line_sl = _parse_service_level(dates, chosen_group, qs)
    # Получение данных для вип линии.
    chosen_group = _get_group_name('vip_line_group_name')
    vip_line_sl = _parse_service_level(dates, chosen_group, qs)
    # Получение данных всех линий.
    chosen_group = _get_group_name('general_group_name')
    general_sl = _parse_service_level(dates, chosen_group, qs)

    return {'sl': {'first_line': first_line_sl, 'vip_line': vip_line_sl,
            'general': general_sl}}


def _parse_aht_level(dates: Dates, chosen_segment: str,
                     qs: Union[models.QuerySet,
                               List[models.Model]]) -> ReportAht:
    """
    Функция для получения данных по отчёту AHT.

    На выходе мы получаем данные:
        - AHT за требуемый день
        - AHT за неделю
        - AHT за месяц

    Args:
        dates (Dates): коллекция дат
        group (str): группа для которой необходима информация
        qs (Union[models.QuerySet, List[models.Model]]): данные из БД

    Returns:
        ReportServiceLevel: коллекция необходимых данных
    """
    if not qs.exists():
        return ReportAht(0, 0, 0, 0)
    # Фильтруем данные для сегмента
    qs_for_month = qs.filter(segment=chosen_segment)
    qs_for_week = qs_for_month.filter(
        date__gte=dates.monday_this_week, date__lte=dates.sunday_this_week)
    qs_for_chosen_day = qs_for_month.filter(
        date=dates.chosen_date)

    # Высчитывание проценты SL
    mountly_aht = sum([report.aht_level
                      for report in qs_for_month]) / len(qs_for_month)
    mountly_aht = int(round(mountly_aht, 0))

    weekly_aht = sum([report.aht_level
                     for report in qs_for_week]) / len(qs_for_week)
    weekly_aht = int(round(weekly_aht, 0))

    dayly_aht = qs_for_chosen_day.first().aht_level
    dayly_aht = int(round(dayly_aht, 0))

    # Расскладываем доп. данные
    issues_received = qs_for_chosen_day.first().issues_received

    return ReportAht(mountly_aht, weekly_aht, dayly_aht, issues_received)


def _get_aht(datestring: str) -> Mapping[Literal['aht'], ReportAht]:
    """Функция для получения данных по отчёту SL для групп.

    На выходе мы получаем данные:
        - AHT за требуемый день
        - AHT за неделю
        - AHT за месяц

    Args:
        datestring (str): строка даты за которую требуется отчет.

    Returns:
        Mapping[Literal['sl'], Mapping[Literal['first_line', 'vip_line',
                                               'general'],
        ReportServiceLevel]]: словарь данных, с ключами по линиям ТП
    """
    today_date = datetime.now().date()
    # Операции над входящей строкой даты
    dates = get_date_collections(datestring)
    # Получение отчетов за месяц
    qs = naumen_services.get_report_to_period('aht', dates.calends_this_month,
                                              dates.calends_next_month)
    # Исключаем нулевые отчеты
    qs = qs.filter(date__lte=today_date)
    # Получение данных для первой линии.
    aht = _parse_aht_level(dates, "AHT", qs)

    return {'aht': aht}


def _parse_mttr_level(dates: Dates,
                      qs: Union[models.QuerySet, List[models.Model]]
                      ) -> ReportMttr:
    """
    Функция для получения данных по отчёту MTTR.

    На выходе мы получаем данные:
        - Общее количество обращений
        - Средний МТТР
        - Средний МТТР ТП за месяц
        - Средний МТТР ТП за неделю
        - Средний МТТР ТП за день

    Args:
        dates (Dates): коллекция дат
        qs (Union[models.QuerySet, List[models.Model]]): данные из БД

    Returns:
        Mapping: словарь входных данных.
    """
    if not qs.exists():
        return ReportMttr(0, 0, 0, 0, 0)
    # Фильтруем данные для сегмент
    qs_for_month = qs
    qs_for_week = qs_for_month.filter(
        date__gte=dates.monday_this_week, date__lte=dates.sunday_this_week)
    qs_for_chosen_day = qs_for_month.filter(
        date=dates.chosen_date)

    # Высчитывание проценты SL
    mountly_mttr_tech_support = sum([report.average_mttr_tech_support.seconds
                                     // 60 for report in qs_for_month]
                                    ) / len(qs_for_month)
    mountly_mttr_tech_support = int(round(mountly_mttr_tech_support, 0))

    weekly_mttr_tech_support = sum([report.average_mttr_tech_support.seconds
                                    // 60 for report in qs_for_week]
                                   ) / len(qs_for_week)
    weekly_mttr_tech_support = int(round(weekly_mttr_tech_support, 0))

    dayly_mttr_tech_support = qs_for_chosen_day.first()\
        .average_mttr_tech_support.seconds // 60
    dayly_mttr_tech_support = int(round(dayly_mttr_tech_support, 0))

    dayly_mttr = qs_for_chosen_day.first().average_mttr.seconds // 60
    dayly_mttr = int(round(dayly_mttr, 0))

    # Расскладываем доп. данные
    num_issues = qs_for_chosen_day.first().total_number_trouble_ticket

    return ReportMttr(num_issues, dayly_mttr, mountly_mttr_tech_support,
                      weekly_mttr_tech_support, dayly_mttr_tech_support)


def _get_mttr(datestring: str) -> Mapping[Literal['mttr'], ReportMttr]:
    """Функция получение данных по отчёту MTTR:

    На вход поступает строка даты, за который необходим отчёт.

    На выходе поступают данные:
        - Общее количество обращений
        - Средний МТТР
        - Средний МТТР ТП за месяц
        - Средний МТТР ТП за неделю
        - Средний МТТР ТП за день

    Args:
        datestring (str): строка даты, за который необходим отчёт.

    Returns:
        Mapping: словарь входных данных.
    """
    today_date = datetime.now().date()
    # Операции над входящей строкой даты
    dates = get_date_collections(datestring)
    qs = naumen_services.get_report_to_period('mttr', dates.calends_this_month,
                                              dates.calends_next_month)
    # Исключаем нулевые отчеты
    qs = qs.filter(date__lte=today_date)
    # Получение данных для первой линии.
    mttr = _parse_mttr_level(dates, qs)
    return {'mttr': mttr}


def _parse_flr_level(dates: Dates,
                     qs: Union[models.QuerySet, List[models.Model]]
                     ) -> ReportFlr:
    """
    Функция для получения данных по отчёту FLR.

    На выходе мы получаем данные:
        - FLR за месяц (в %)
        - FLR за неделю (в %)
        - FLR за день (в %)
        - Количество обращений закрытых без других отделов
        - Количество первичных обращений

    Args:
        dates (Dates): коллекция дат
        qs (Union[models.QuerySet, List[models.Model]]): данные из БД

    Returns:
        ReportFlr: коллекция необходимых данных
    """
    if not qs.exists():
        return ReportFlr(0, 0, 0, 0, 0)
    # Фильтруем данные для сегмента
    qs_for_month = qs
    qs_for_week = qs_for_month.filter(
        date__gte=dates.monday_this_week, date__lte=dates.sunday_this_week)
    qs_for_chosen_day = qs_for_month.filter(
        date=dates.chosen_date)

    # Высчитывание проценты FLR
    monthly_tickets_closed_independently = sum(
        [report.number_trouble_ticket_closed_independently
         for report in qs_for_month])
    monthly_tickets_primary_closed = sum(
        [report.number_primary_trouble_tickets
         for report in qs_for_month])
    mountly_flr = 100.0

    if monthly_tickets_primary_closed:
        mountly_flr = (monthly_tickets_closed_independently /
                       monthly_tickets_primary_closed) * 100
    mountly_flr = int(round(mountly_flr, 0))

    weekly_tickets_closed_independently = sum(
        [report.number_trouble_ticket_closed_independently
         for report in qs_for_week])
    weekly_tickets_primary_closed = sum(
        [report.number_primary_trouble_tickets
         for report in qs_for_week])
    weekly_flr = 100.0

    if weekly_tickets_primary_closed:
        weekly_flr = (weekly_tickets_closed_independently /
                      weekly_tickets_primary_closed) * 100
    weekly_flr = int(round(weekly_flr, 0))

    dayly_flr = 100.0
    if qs_for_chosen_day.first().number_primary_trouble_tickets:
        dayly_flr = qs_for_chosen_day.first().flr_level
    dayly_flr = int(round(dayly_flr, 0))

    # Расскладываем доп. данные
    num_issues_closed_independently = qs_for_chosen_day.first()\
        .number_trouble_ticket_closed_independently
    num_primary_issues = qs_for_chosen_day.first()\
        .number_primary_trouble_tickets

    return ReportFlr(mountly_flr, weekly_flr, dayly_flr,
                     num_issues_closed_independently, num_primary_issues)


def _get_flr(datestring: str) -> Mapping[Literal['flr'], ReportFlr]:
    """Функция получение данных по отчёту FLR:

    На вход поступает строка даты, за который необходим отчёт.

    На выходе поступают данные:
        - FLR за месяц (в %)
        - FLR за неделю (в %)
        - FLR за день (в %)
        - Количество обращений закрытых без других отделов
        - Количество первичных обращений

    Args:
        datestring (str): строка даты, за который необходим отчёт.

    Returns:
        Mapping: словарь входных данных.
    """
    today_date = datetime.now().date()
    # Операции над входящей строкой даты
    dates = get_date_collections(datestring)
    qs = naumen_services.get_report_to_period('flr', dates.calends_this_month,
                                              dates.calends_next_month)
    # Исключаем нулевые отчеты
    qs = qs.filter(date__lte=today_date)
    # Формируем данные
    flr = _parse_flr_level(dates, qs)
    return {'flr': flr}


def get_load_ratings() -> Union[models.QuerySet, List[models.Model]]:
    """
    Функция получения номинальных значений нагрузки на группу.

    Returns:
        Union[models.QuerySet, List[models.Model]]:
            номинальные значения нагрузки
    """
    obj, created = RatingSetting.objects.get_or_create(is_active=True)

    return obj


def get_load_naumen_settings() -> Union[models.QuerySet, List[models.Model]]:
    """
    Функция получения наименований групп и шагов.

    Returns:
        Union[models.QuerySet, List[models.Model]]:
            наименования групп и шагов.
    """
    obj, created = NaumenSetting.objects.get_or_create(is_active=True)

    return obj


def _compare_num(first: int, second: int) -> Union[float, None]:
    """
    Функция первого числа со вторым.

    На вход функция получает два числа.

    На выход передает процент до тождественности для первого числа со вторым
    или None в случае невозможности вычисления

    Args:
        first (int): первое число
        second (int): второе число

    Returns:
        Union[float, None]: процент до тождественности или None
    """
    num_type_check = all([isinstance(first, int), isinstance(second, int)])

    if not num_type_check:
        return None

    if second == 0:
        # Если втрое число 0, то первое больше него на 100%
        return 100.0

    if first == second:
        return 0.0

    return round((first / second * 100) - 100, 1)


def _sl_analytics(chosen_day: Mapping[Literal['sl'], Mapping],
                  nominal_values: Union[models.QuerySet, List[models.Model]],
                  comparison_day: Mapping[Literal['sl'], Mapping] = {}
                  ) -> Mapping[Literal['sl'], Mapping]:
    """
    Функция сравнения данных sl, с номинальными и с переданным днем.

    На вход, функция получает отчёт sl, который необходимо сравнить.
    При необходимости можно передать дополнительный день сравнения.

    На выходе функция отдает модифицированный словарь аналитики sl

    Args:
        chosen_day (Mapping[Literal['sl'], Mapping]):
            дневной отчёт sl, который необходимо сравнить
        nominal_values: Union[models.QuerySet, List[models.Model]]:
            номинальные значения нагрузки
        comparison_day (Mapping[Literal['sl'], Mapping]):
            дополнительный день сравнения. По умол. {}

    Returns:
        Mapping[Literal['analytics'], Mapping]: словарь аналитики sl

    """
    # Структура выходного словаря
    analytics_dict = {
        'sl': {
            'first_line': RatingAnalytics(0.0, 0.0),
            'vip_line': RatingAnalytics(0.0, 0.0),
            'general': RatingAnalytics(0.0, 0.0),
        }
    }
    # Аналитика относительно дня сравнения если день не передан
    rating_to_comparison_first = 0.0
    rating_to_comparison_vip = 0.0
    rating_to_comparison_general = 0.0

    # Аналитики относительно номинальных значений.
    rating_to_nominal_first = _compare_num(
        chosen_day['sl']['first_line'].num_issues,
        nominal_values.num_issues_first_line)

    rating_to_nominal_vip = _compare_num(
        chosen_day['sl']['vip_line'].num_issues,
        nominal_values.num_issues_vip_line)

    rating_to_nominal_general = _compare_num(
        chosen_day['sl']['general'].num_issues,
        nominal_values.num_issues_general)

    # Аналитика относительно дня сравнения
    if comparison_day:
        rating_to_comparison_first = _compare_num(
            chosen_day['sl']['first_line'].num_issues,
            comparison_day['sl']['first_line'].num_issues)

        rating_to_comparison_vip = _compare_num(
            chosen_day['sl']['vip_line'].num_issues,
            comparison_day['sl']['vip_line'].num_issues)

        rating_to_comparison_general = _compare_num(
            chosen_day['sl']['general'].num_issues,
            comparison_day['sl']['general'].num_issues)

    analytics_dict['sl']['first_line'] = RatingAnalytics(
        rating_to_nominal_first, rating_to_comparison_first
    )
    analytics_dict['sl']['vip_line'] = RatingAnalytics(
        rating_to_nominal_vip, rating_to_comparison_vip
    )
    analytics_dict['sl']['general'] = RatingAnalytics(
        rating_to_nominal_general, rating_to_comparison_general
    )

    return analytics_dict


def _mttr_analytics(chosen_day: Mapping[Literal['mttr'], ReportMttr],
                    nominal_values: Union[models.QuerySet, List[models.Model]],
                    comparison_day: Mapping[Literal['mttr'], ReportMttr] = {}
                    ) -> Mapping[Literal['mttr'], RatingAnalytics]:
    """
    Функция сравнения данных mttr, с номинальными и с переданным днем.

    На вход, функция получает отчёт mttr, который необходимо сравнить.
    При необходимости можно передать дополнительный день сравнения.

    На выходе функция отдает модифицированный словарь аналитики mttr

    Args:
        chosen_day (Mapping[Literal['mttr'], ReportMttr]):
            дневной отчёт mttr, который необходимо сравнить
        nominal_values: Union[models.QuerySet, List[models.Model]]:
            номинальные значения нагрузки
        comparison_day (Mapping[Literal['mttr'], ReportMttr]):
            дополнительный день сравнения. По умол. {}

    Returns:
        Mapping[Literal['mttr'], RatingAnalytics]: словарь аналитики mttr

    """
    # Структура выходного словаря
    analytics_dict = {
        'mttr': RatingAnalytics(0.0, 0.0),
    }
    # Аналитика относительно дня сравнения если день не передан
    rating_to_comparison = 0.0

    # Аналитики относительно номинальных значений.
    rating_to_nominal = _compare_num(chosen_day['mttr'].num_issues,
                                     nominal_values.num_issues_closed)

    # Аналитика относительно дня сравнения
    if comparison_day:
        rating_to_comparison = _compare_num(chosen_day['mttr'].num_issues,
                                            comparison_day['mttr'].num_issues)

    analytics_dict['mttr'] = RatingAnalytics(rating_to_nominal,
                                             rating_to_comparison)

    return analytics_dict


def _flr_analytics(chosen_day: Mapping[Literal['flr'], ReportFlr],
                   nominal_values: Union[models.QuerySet, List[models.Model]],
                   comparison_day: Mapping[Literal['flr'], ReportFlr] = {}
                   ) -> Mapping[Literal['flr'], RatingAnalytics]:
    """
    Функция сравнения данных flr, с номинальными и с переданным днем.

    На вход, функция получает отчёт flr, который необходимо сравнить.
    При необходимости можно передать дополнительный день сравнения.

    На выходе функция отдает модифицированный словарь аналитики flr

    Args:
        chosen_day (Mapping[Literal['flr'], ReportFlr]):
            дневной отчёт flr, который необходимо сравнить
        nominal_values: Union[models.QuerySet, List[models.Model]]:
            номинальные значения нагрузки
        comparison_day (Mapping[Literal['flr'], ReportFlr]):
            дополнительный день сравнения. По умол. {}

    Returns:
        Mapping[Literal['flr'], RatingAnalytics]: словарь аналитики flr

    """
    # Структура выходного словаря
    analytics_dict = {
        'flr': RatingAnalytics(0.0, 0.0),
    }
    # Аналитика относительно дня сравнения если день не передан
    rating_to_comparison = 0.0

    # Аналитики относительно номинальных значений.
    rating_to_nominal = _compare_num(chosen_day['flr'].num_primary_issues,
                                     nominal_values.num_primary_issues)

    # Аналитика относительно дня сравнения
    if comparison_day:
        rating_to_comparison = _compare_num(
            chosen_day['flr'].num_primary_issues,
            comparison_day['flr'].num_primary_issues)

    analytics_dict['flr'] = RatingAnalytics(rating_to_nominal,
                                            rating_to_comparison)

    return analytics_dict


def _aht_analytics(chosen_day: Mapping[Literal['aht'], ReportAht],
                   nominal_values: Union[models.QuerySet, List[models.Model]],
                   comparison_day: Mapping[Literal['aht'], ReportAht] = {}
                   ) -> Mapping[Literal['aht'], RatingAnalytics]:
    """
    Функция сравнения данных aht, с номинальными и с переданным днем.

    На вход, функция получает отчёт aht, который необходимо сравнить.
    При необходимости можно передать дополнительный день сравнения.

    На выходе функция отдает модифицированный словарь аналитики aht

    Args:
        chosen_day (Mapping[Literal['aht'], ReportAht]):
            дневной отчёт flr, который необходимо сравнить
        nominal_values: Union[models.QuerySet, List[models.Model]]:
            номинальные значения нагрузки
        comparison_day (Mapping[Literal['aht'], ReportAht]):
            дополнительный день сравнения. По умол. {}

    Returns:
        Mapping[Literal['aht'], RatingAnalytics]: словарь аналитики aht

    """
    # Структура выходного словаря
    analytics_dict = {
        'aht': RatingAnalytics(0.0, 0.0),
    }
    # Аналитика относительно дня сравнения если день не передан
    rating_to_comparison = 0.0

    # Аналитики относительно номинальных значений.
    rating_to_nominal = _compare_num(chosen_day['aht'].issues_received,
                                     nominal_values.issues_received)
    # Аналитика относительно дня сравнения
    if comparison_day:
        rating_to_comparison = _compare_num(
            chosen_day['aht'].issues_received,
            comparison_day['aht'].issues_received)

    analytics_dict['aht'] = RatingAnalytics(rating_to_nominal,
                                            rating_to_comparison)

    return analytics_dict


def analytics(chosen_day: dict[Literal['sl', 'mttr', 'flr'], Mapping],
              comparison_day: Mapping[Literal['sl', 'mttr', 'flr'], Mapping] = {}
              ) -> dict[Literal['sl', 'mttr', 'flr', 'analytics'], Mapping]:
    """
    Функция сравнения данных, с номинальными и с переданным днем.

    На вход, функция получает дневной отчёт, который необходимо сравнить.
    При необходимости можно передать дополнительный день сравнения.

    На выходе функция отдает модифицированный словарь с долнительным
    ключем выполненного сравнения.

    Args:
        chosen_day (dict[Literal['sl', 'mttr', 'flr'], Mapping]):
            дневной отчёт, который необходимо сравнить
        comparison_day (Mapping[Literal['sl', 'mttr', 'flr'], Mapping]):
            дополнительный день сравнения. По умол. {}

    Returns:
        dict[Literal['sl', 'mttr', 'flr', 'analytics'], Mapping]:
        модифицированный словарь
        с долнительным ключем выполненного сравнения.

    """
    nominal_values = get_load_ratings()
    modificated_day = chosen_day.copy()
    sl_analytics_dict = _sl_analytics(chosen_day, nominal_values,
                                      comparison_day)
    mttr_analytics_dict = _mttr_analytics(chosen_day, nominal_values,
                                          comparison_day)
    flr_analytics_dict = _flr_analytics(chosen_day, nominal_values,
                                        comparison_day)
    aht_analytics_dict = _aht_analytics(chosen_day, nominal_values,
                                        comparison_day)
    modificated_day.update(
        {'analytics': {**sl_analytics_dict, **mttr_analytics_dict,
                       **flr_analytics_dict, **aht_analytics_dict}}
        )
    return modificated_day


def get_dashboard_data(datestring: str) -> Mapping:
    """Главная функция получения данных для view дашборда.

    Вызывает все дополнительные функции и отдает ассоциативный словарь данных
    контекста необходимых для view.

    На вход поступает строка даты, за который необходим отчёт.

    На выходе поступают данные:
        - SL за требуемый день по первой линии
        - Количество поступивших обращений на первую линию
        - Количество первичных обращений на первой линии
        - Количество обращений принятых до крайнего срока на первой линии
        - Количество обращений принятых после крайнего срока на первой линии
        - SL за требуемый день по вип линии
        - Количество поступивших обращений на вип линию
        - Количество первичных обращений на вип линии
        - Количество обращений принятых до крайнего срока на вип линии
        - Количество обращений принятых после крайнего срока на вип линии
        - Итоговый SL за требуемый день
        - Количество поступивших обращений итоговое
        - Количество первичных обращений итоговое
        - Количество обращений принятых до крайнего срока итоговое
        - Количество обращений принятых после крайнего срока итоговое
        - SL за неделю по первой линии
        - SL за неделю по вип линии
        - Итоговый SL за неделю
        - SL за месяц по первой линии
        - SL за месяц по вип линии
        - Итоговый SL за месяц
        - MTTR за требуемый день
        - FLR требуемый день
        - Аналитика нагрузки относительно номинальных значений

    Args:
        datestring (str): строка даты, за который необходим отчёт.

    Returns:
        Mapping: словарь входных данных.
    """
    service_level_dict = _get_service_level(datestring)
    mttr_dict = _get_mttr(datestring)
    flr_dict = _get_flr(datestring)
    aht_dict = _get_aht(datestring)
    day_report = {**service_level_dict, **mttr_dict, **flr_dict, **aht_dict}
    return day_report


def get_day_dates_and_data(datestring: Literal['%Y-%m-%d'] = None) -> dict[
        Literal['dates', 'dashboard_data'], Any]:
    """
    Функция для получения дневного отчета для view.

    Возвращает:
        Данные за день и аналитику относительно предыдущего дня
        и номинальных значений нагрузки.
    """
    if datestring is None:
        datestring = datetime.now().date().isoformat()

    dates = get_date_collections(datestring)
    dashboard_data = get_dashboard_data(dates.chosen_date.isoformat())
    # before_day_data = get_dashboard_data(dates.before_day.isoformat())
    before_day_data = {}
    dashboard_data = analytics(dashboard_data, before_day_data)
    return {'dates': dates, 'dashboard_data': dashboard_data}


def get_day_report(desired_date: Literal['%Y-%m-%d'],
                   comparison_date: Literal['%Y-%m-%d']) -> dict[
        Literal['desired_date', 'comparison_date'], Any]:
    """
    Функция для получения дневного отчета для view вкалдки reports.

    Возвращает:
        Данные за день и аналитику относительно выбранного дня
        и номинальных значений нагрузки.
    """

    desired_dates = get_date_collections(desired_date)
    comparison_dates = get_date_collections(comparison_date)
    desired_date_data = get_dashboard_data(
        desired_dates.chosen_date.isoformat())
    comparison_date_data = get_dashboard_data(
        comparison_dates.chosen_date.isoformat())
    desired_date_data = analytics(desired_date_data, comparison_date_data)
    return {'desired_date': desired_date_data,
            'comparison_date': comparison_date_data}


def issues_on_group():
    """
    Функция для получения количества тикетов на группах.

    Returns:
        (dict): словарь с счетчиками.
    """
    first_line_count = len(naumen_services.get_issues_from_db(
        **{'responsible': _get_group_name('first_line_group_name'),
           'step': _get_group_step_name()}))
    vip_line_count = len(naumen_services.get_issues_from_db(
        **{'responsible': _get_group_name('vip_line_group_name'),
           'step': _get_group_step_name()}))
    return {'first_line_counter': first_line_count,
            'vip_line_counter': vip_line_count}
