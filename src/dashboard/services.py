from datetime import date, datetime, time, timedelta

from naumen.services import add_months


first_line_group_name = 'Группа поддержки и управления сетью  (Напр ТП В2В)'
vip_line_group_name = 'Группа поддержки VIP - клиентов (Напр ТП В2В)'


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
