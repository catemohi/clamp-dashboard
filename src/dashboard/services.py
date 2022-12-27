from datetime import date, datetime, time, timedelta
from typing import Literal, Collection


from naumen.services import add_months, get_report_to_period





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


def convert_datestr_to_datetime_obj(date_str: str) -> datetime:
    """Функция конвертации строки даты в datetime обьект

    Args:
        date_str (str): строка даты

    Returns:
        datetime: обьект даты и времени
    """

    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    datetime_obj = datetime.combine(date, time(13, 0))
    return datetime_obj


# TODO новая функция которая считает количество тикетов
def get_trouble_ticket_count_from_db():
    return {'trouble_ticket_counter': 99, 'trouble_ticket_vip_counter': 99}


def get_group_name(required_group: Literal['first_line_group_name',
                                           'vip_line_group_name']) -> str:
    """
    Функция получения названия группы ТП

    Args:
        required_group (Literal[first_line_group_name, vip_line_group_name]): 
        какую группу необходимо получить.

    Returns:
        str: название группы или пустую строку
    """
    # TODO обращение к таблице с хранением имен групп
    FIRST_LINE_GROUP = 'Группа поддержки и управления сетью  (Напр ТП В2В)'
    VIP_LINE_GROUP = 'Группа поддержки VIP - клиентов (Напр ТП В2В)'

    if required_group == 'first_line_group_name':
        return FIRST_LINE_GROUP

    if required_group == 'vip_line_group_name':
        return VIP_LINE_GROUP

    return ''


def get_date_collections(datestring: str) -> Collection[date]:
    """Функция для возврата коллекции дат.

    На выходе мы получаем коллекцию дат:
        - первое число месяца передоваемой даты
        - первое число следующего месяца
        - число начала недели
        - число конца недели
        - требуемая дата

    Args:
        datestring (str): строка даты от которой требуется выдать коллекцию

    Returns:
        Collection[date]: коллекция дат.
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

    return (first_day_month, first_day_next_month, monday_this_week,
            sunday_this_week, chosen_date)


def get_service_level(datestring: str) -> Collection:
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
        Collection: _description_
    """
    # Операции над входящей строкой даты
    dates = get_date_collections(datestring)
    # Получение данных для первой линии.
    chosen_group = get_group_name('first_line_group_name')
    # TODO 