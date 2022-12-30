from datetime import date, datetime, time, timedelta
from json import JSONEncoder
from typing import Literal, NamedTuple, Mapping
from typing import Union, List, Any

from django.db import models

from naumen.services import add_months, get_report_to_period


# TODO https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-date
def get_name_month(number_month: int):
    """Функция которая возвращает название месяца.

    Args:
        number_month (int): номер месяца

    Returns:
        str: название месяца
    """
    name_month = [
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь ',
    ]
    return name_month[number_month-1]


def get_params(desired_date: datetime):
    today_data = {}
    # desired_date = desired_date - timedelta(days=0)

    today_date = desired_date.date()
    from_monday_days_passed = datetime.isoweekday(desired_date) - 1
    days_until_sunday = 7 - datetime.isoweekday(desired_date)

    monday_this_week = (desired_date -
                        timedelta(days=from_monday_days_passed)).date()

    sunday_this_week = (desired_date +
                        timedelta(days=days_until_sunday)).date()

    first_day_this_month = date(desired_date.year, desired_date.month, 1)
    first_day_next_month = add_months(first_day_this_month, 1)

    last_day_this_month = (datetime.combine(
        first_day_next_month, time(1, 1)) - timedelta(days=1)).date()

    # TODO новая функция вызова данных отчета MTTR
    # day_mttr = get_day_mttr(desired_date)

    # TODO новая функция вызова данных отчета SL по группе
    # day_first_line_sl = get_day_service_level_group(today_date,
    #                                                 first_line_group_name)

    # TODO новая функция вызова данных отчета SL по группе
    # day_service_level_vip_line = get_day_service_level_group(today_date,
    #                                                          vip_line_group_name)

    # TODO новая функция вызова данных отчета FLR
    # day_flr = get_day_flr(desired_date)

    # today_data['DayMttr'] = int(day_mttr)
    today_data['DayMttr'] = 100

    # today_data['DayFlr'] = int(day_flr.flr_level)
    today_data['DayFlr'] = 100

    # today_data['DayServiceLevelFirstLine'] = int(
    #     day_service_level_first_line.service_level)
    today_data['DayServiceLevelFirstLine'] = 100

    # today_data['DayServiceLevelVipLine'] = int(
    #     day_service_level_vip_line.service_level)
    today_data['DayServiceLevelVipLine'] = 100

    today_data['WeeklyServiceLevelFirstLine'] = 100
    # TODO новая функция подсчета недельного SL по группе
    # today_data['WeeklyServiceLevelFirstLine'] = \
    #     get_range_days_service_level_group(monday_this_week,
    #                                        sunday_this_week,
    #                                        first_line_group_name)
    today_data['WeeklyServiceLevelVipLine'] = 100
    # TODO новая функция подсчета недельного SL по группе
    # today_data['WeeklyServiceLevelVipLine'] = \
    #     get_range_days_service_level_group(monday_this_week,
    #                                        sunday_this_week,
    #                                        vip_line_group_name)
    today_data['MonthlyServiceLevelFirstLine'] = 100
    # TODO новая функция подсчета месячного SL по группе
    # today_data['MonthlyServiceLevelFirstLine'] = \
    #     get_range_days_service_level_group(first_day_this_month,
    #                                        last_day_this_month,
    #                                        first_line_group_name)
    today_data['MonthlyServiceLevelVipLine'] = 100
    # TODO новая функция подсчета месячного SL по группе
    # today_data['MonthlyServiceLevelVipLine'] = \
    #     get_range_days_service_level_group(first_day_this_month,
    #                                        last_day_this_month,
    #                                        vip_line_group_name)
    today_data['NameMonth'] = get_name_month(desired_date.month)

    today_data['Week'] = (f'{monday_this_week.strftime("%d.%m")} - '
                          f'{sunday_this_week.strftime("%d.%m")}')

    today_data['Today'] = today_date.strftime("%d.%m.%y")

    return today_data


# TODO новая функция которая считает количество тикетов
def get_trouble_ticket_count_from_db():
    return {'trouble_ticket_counter': 99, 'trouble_ticket_vip_counter': 99}

###############################################################################


class CustomEncoder(JSONEncoder):
    """
    Кастомный енкодер JSON для NamedTuple и DateTime

    """
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date, time)):
            return o.strftime('%d.%m.%Y')
        elif isinstance(o, timedelta):
            return o.seconds()
        return super().default(o)


class Dates(NamedTuple):
    """Класс для хранения коллекции дат.

    Хранит даты:
        - первое число месяца передоваемой даты
        - первое число следующего месяца
        - число начала недели
        - число конца недели
        - требуемая дата

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
        - Средний МТТР ТП'
    """
    num_issues: int
    average_mttr: int
    average_mttr_tech_support: int


class ReportFlr(NamedTuple):
    """Класс для хранения отчета по MTTR

    Хранит данные:
        - FLR за день (в %)
        - Количество обращений закрытых без других отделов
        - Количество первичных обращений
    """
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
        elif isinstance(obj, (datetime, date, time)):
            obj = obj.strftime('%d.%m.%Y')
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
    # TODO обращение к таблице с хранением имен групп
    FIRST_LINE_GROUP = 'Группа поддержки и управления сетью  (Напр ТП В2В)'
    VIP_LINE_GROUP = 'Группа поддержки VIP - клиентов (Напр ТП В2В)'
    GENERAL_GROUP = 'Итог'

    if required_group == 'first_line_group_name':
        return FIRST_LINE_GROUP

    if required_group == 'vip_line_group_name':
        return VIP_LINE_GROUP

    if required_group == 'general_group_name':
        return GENERAL_GROUP

    return ''


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
    first_day_next_month = add_months(first_day_month, 1)

    _monday_days_passed = datetime.isoweekday(chosen_date) - 1
    monday_this_week = (chosen_datetime -
                        timedelta(days=_monday_days_passed)).date()

    _until_sunday = 7 - datetime.isoweekday(chosen_date)
    sunday_this_week = (chosen_datetime + timedelta(days=_until_sunday)).date()

    next_day = chosen_date + timedelta(days=1)
    before_day = chosen_date - timedelta(days=1)

    return Dates(first_day_month, first_day_next_month, monday_this_week,
                 sunday_this_week, chosen_date, next_day, before_day)


def _parse_service_level(dates: Dates, chosen_group: str,
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
        ReportServiceLevel(0, 0, 0, 0, 0, 0, 0)
    # Фильтруем данные для группы
    qs_for_month = qs.filter(name_group=chosen_group)
    qs_for_week = qs_for_month.filter(
        date__gte=dates.monday_this_week, date__lte=dates.sunday_this_week)
    qs_for_chosen_day = qs_for_month.filter(
        date=dates.chosen_date)

    # Высчитывание проценты SL
    mountly_sl = sum([report.service_level
                      for report in qs_for_month]) / len(qs_for_month)
    mountly_sl = int(round(mountly_sl, 0))

    weekly_sl = sum([report.service_level
                     for report in qs_for_week]) / len(qs_for_week)
    weekly_sl = int(round(weekly_sl, 0))

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
    qs = get_report_to_period('sl', dates.calends_this_month,
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


def _get_mttr(datestring: str) -> Mapping[Literal['mttr'], ReportMttr]:
    """Функция получение данных по отчёту MTTR:

    На вход поступает строка даты, за который необходим отчёт.

    На выходе поступают данные:
        - Общее количество обращений
        - Средний МТТР
        - Средний МТТР ТП'

    Args:
        datestring (str): строка даты, за который необходим отчёт.

    Returns:
        Mapping: словарь входных данных.
    """
    # Операции над входящей строкой даты
    dates = get_date_collections(datestring)
    qs = get_report_to_period('mttr', dates.chosen_date, dates.next_day)
    if not qs.exists():
        return {'mttr': ReportMttr(0, 0, 0)}
    # Формируем данные
    num_issues = qs.first().total_number_trouble_ticket
    average_mttr = qs.first().average_mttr.seconds
    average_mttr_tech_support = qs.first().average_mttr_tech_support.seconds
    mttr_report = ReportMttr(num_issues, average_mttr,
                             average_mttr_tech_support)
    return {'mttr': mttr_report}


def _get_flr(datestring: str) -> Mapping[Literal['flr'], ReportFlr]:
    """Функция получение данных по отчёту MTTR:

    На вход поступает строка даты, за который необходим отчёт.

    На выходе поступают данные:
        - FLR за день (в %)
        - Количество обращений закрытых без других отделов
        - Количество первичных обращений

    Args:
        datestring (str): строка даты, за который необходим отчёт.

    Returns:
        Mapping: словарь входных данных.
    """
    # Операции над входящей строкой даты
    dates = get_date_collections(datestring)
    qs = get_report_to_period('flr', dates.chosen_date, dates.next_day)
    if not qs.exists():
        {'flr': ReportFlr(0, 0, 0)}
    # Формируем данные
    level = int(round(qs.first().flr_level, 0))
    num_issues_closed_independently = qs.first().\
        number_trouble_ticket_closed_independently
    num_primary_issues = qs.first().number_primary_trouble_tickets

    flr_report = ReportFlr(level, num_issues_closed_independently,
                           num_primary_issues)
    return {'flr': flr_report}


def _get_load_ratings() -> Union[models.QuerySet, List[models.Model]]:
    """
    Функция получения номинальных значений нагрузки на группу.

    Returns:
        Union[models.QuerySet, List[models.Model]]:
            номинальные значения нагрузки
    """
    # TODO запрос к таблице показателей
    # Пока сделаем подменную структуру данных
    class LoadRatings(NamedTuple):
        service_level: int
        average_mttr_tech_support: int
        flr_level: int
        num_issues_first_line: int
        num_issues_vip_line: int
        num_issues_general: int
        num_issues_closed: int
        num_primary_issues: int
    return LoadRatings(80, 50, 50, 80, 40, 120, 70, 40)


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
            'first_line': None,
            'vip_line': None,
            'general': None
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
        'mttr': None
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
        'flr': None
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
    nominal_values = _get_load_ratings()
    modificated_day = chosen_day.copy()
    sl_analytics_dict = _sl_analytics(chosen_day, nominal_values,
                                      comparison_day)
    mttr_analytics_dict = _mttr_analytics(chosen_day, nominal_values,
                                          comparison_day)
    flr_analytics_dict = _flr_analytics(chosen_day, nominal_values,
                                        comparison_day)
    modificated_day.update(
        {'analytics': {**sl_analytics_dict, **mttr_analytics_dict,
                       **flr_analytics_dict}}
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
    day_report = {**service_level_dict, **mttr_dict, **flr_dict}
    return day_report
