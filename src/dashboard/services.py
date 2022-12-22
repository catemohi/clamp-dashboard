from datetime import datetime, timedelta,date,time
from itertools import count
from django.db.models import Sum

from reports.services import *
from trouble_ticket_table.services import *

first_line_group_name = 'Группа поддержки и управления сетью  (Напр ТП В2В)'
vip_line_group_name = 'Группа поддержки VIP - клиентов (Напр ТП В2В)'

def get_params(desired_date):
    today_data = {}
    desired_date = desired_date - timedelta(days=0)
    number_of_days_from_monday = datetime.isoweekday(desired_date) - 1
    number_of_days_until_sunday = (7 - datetime.isoweekday(desired_date))
    today_date = desired_date.date()
    monday_of_this_week = (desired_date - timedelta(days=number_of_days_from_monday)).date()
    sunday_of_this_week = (desired_date + timedelta(days=number_of_days_until_sunday)).date()
    first_day_of_this_month = date(desired_date.year, desired_date.month, 1)
    first_day_of_next_month = date(desired_date.year,desired_date.month + 1, 1)
    last_day_of_this_month = (datetime.combine(first_day_of_next_month, time(1,1)) - timedelta(days=1)).date()
    day_mttr = get_day_mttr(desired_date)

    day_service_level_first_line = get_day_service_level_group(today_date, first_line_group_name)
    day_service_level_vip_line = get_day_service_level_group(today_date, vip_line_group_name)
    day_flr = get_day_flr(desired_date)
    today_data['DayMttr'] = int(day_mttr)
    today_data['DayFlr'] = int(day_flr.flr_level)
    today_data['DayServiceLevelFirstLine'] = int(day_service_level_first_line.service_level)
    today_data['DayServiceLevelVipLine'] = int(day_service_level_vip_line.service_level)
    today_data['WeeklyServiceLevelFirstLine'] = get_range_days_service_level_group(
        monday_of_this_week, sunday_of_this_week, first_line_group_name)
    today_data['WeeklyServiceLevelVipLine'] = get_range_days_service_level_group(
        monday_of_this_week, sunday_of_this_week, vip_line_group_name)
    today_data['MonthlyServiceLevelFirstLine'] = get_range_days_service_level_group(
        first_day_of_this_month,last_day_of_this_month, first_line_group_name)
    today_data['MonthlyServiceLevelVipLine'] = get_range_days_service_level_group(
        first_day_of_this_month,last_day_of_this_month, vip_line_group_name)
    today_data['NameMonth'] = get_name_month(
        desired_date.month)
    today_data['Week'] = f'{monday_of_this_week.strftime("%d.%m")} - {sunday_of_this_week.strftime("%d.%m")}'
    today_data['Today'] = today_date.strftime("%d.%m.%y")
    return today_data


def get_name_month(number_month):
    name_month = [
        'Январь',
        'Февраль' ,
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь' ,
        'Ноябрь',
        'Декабрь ',
    ]
    return name_month[number_month-1]

def get_date_obj(date_str):
    date_part = datetime.strptime(date_str,"%Y-%m-%d").date()
    return datetime.combine(date_part, time(13,0))

def get_trouble_ticket_from_db():
    tickets_list = get_trouble_ticket_collection_from_db()
    return tickets_list

def get_trouble_ticket_count_from_db():
    counter, vip_counter = get_trouble_ticket_count()
    return {'trouble_ticket_counter': counter, 'trouble_ticket_vip_counter': vip_counter}

def get_day_params_and_analytics(desired_date, comparison_date):
    day_params_and_analytics = day_report(
        desired_date, comparison_date, {'first': first_line_group_name, 'vip': vip_line_group_name})
    content = []
    content.append(
        {'number': 1,
        'name': 'Дата',
        'desired_date': desired_date.strftime("%d.%m.%Y"),
        'comparison_date': comparison_date.strftime("%d.%m.%Y")}
    )
    content.append(
        {'number': 2,
        'name': 'Количество обращений за день на первую линию',
        'desired_date': day_params_and_analytics['service level']['today']['first line']['tt to day'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['first line']['tt to day'],}
    )
    content.append(
        {'number': 3,
        'name': 'Количество обращений первой линии принятых вовремя',
        'desired_date': day_params_and_analytics['service level']['today']['first line']['tt taken before deadline'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['first line']['tt taken before deadline'],}
    )
    content.append(
        {'number': 4,
        'name': 'Количество обращений первой линии принятых после срока',
        'desired_date': day_params_and_analytics['service level']['today']['first line']['tt taken after deadline'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['first line']['tt taken after deadline'],}
    )
    content.append(
        {'number': 5,
        'name': 'Нагрузка первой линии относительно нормы',
        'desired_date': day_params_and_analytics['service level']['analytics']['first line']['load relative norm'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 6,
        'name': 'Нагрузка первой линии относительно дня сравнения',
        'desired_date': day_params_and_analytics['service level']['analytics']['first line']['load relative comparison day'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 7,
        'name': 'Service Level первой линии',
        'desired_date': day_params_and_analytics['service level']['today']['first line']['service_level'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['first line']['service_level'],}
    )

    content.append(
        {'number': 8,
        'name': 'Количество обращений за день на вип линию',
        'desired_date': day_params_and_analytics['service level']['today']['vip line']['tt to day'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['vip line']['tt to day'],}
    )
    content.append(
        {'number': 9,
        'name': 'Количество обращений вип линии принятых вовремя',
        'desired_date': day_params_and_analytics['service level']['today']['vip line']['tt taken before deadline'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['vip line']['tt taken before deadline'],}
    )
    content.append(
        {'number': 10,
        'name': 'Количество обращений вип линии принятых после срока',
        'desired_date': day_params_and_analytics['service level']['today']['vip line']['tt taken after deadline'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['vip line']['tt taken after deadline'],}
    )
    content.append(
        {'number': 11,
        'name': 'Нагрузка вип линии относительно нормы',
        'desired_date': day_params_and_analytics['service level']['analytics']['vip line']['load relative norm'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 12,
        'name': 'Нагрузка вип линии относительно дня сравнения',
        'desired_date': day_params_and_analytics['service level']['analytics']['vip line']['load relative comparison day'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 13,
        'name': 'Service Level вип линии',
        'desired_date': day_params_and_analytics['service level']['today']['vip line']['service_level'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['vip line']['service_level'],}
    )

    content.append(
        {'number': 14,
        'name': 'Общее количество обращений за день',
        'desired_date': day_params_and_analytics['service level']['today']['general']['tt to day'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['general']['tt to day'],}
    )
    content.append(
        {'number': 15,
        'name': 'Общее количество обращений принятых вовремя',
        'desired_date': day_params_and_analytics['service level']['today']['general']['tt taken before deadline'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['general']['tt taken before deadline'],}
    )
    content.append(
        {'number': 16,
        'name': 'Общее количество обращений принятых после срока',
        'desired_date': day_params_and_analytics['service level']['today']['general']['tt taken after deadline'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['general']['tt taken after deadline'],}
    )
    content.append(
        {'number': 17,
        'name': 'Общая нагрузка относительно нормы',
        'desired_date': day_params_and_analytics['service level']['analytics']['general']['load relative norm'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 18,
        'name': 'Общая нагрузка относительно дня сравнения',
        'desired_date': day_params_and_analytics['service level']['analytics']['general']['load relative comparison day'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 19,
        'name': 'Общий Service Level',
        'desired_date': day_params_and_analytics['service level']['today']['general']['service_level'],
        'comparison_date': day_params_and_analytics['service level']['comparison day']['general']['service_level'],}
    )

    content.append(
        {'number': 20,
        'name': 'MTTR',
        'desired_date': str(timedelta(
            seconds=day_params_and_analytics['mttr']['today']['mttr'])),
        'comparison_date': str(timedelta(
            seconds=day_params_and_analytics['mttr']['comparison day']['mttr'])),}
        )
    content.append(
        {'number': 21,
        'name': 'Общее количество закрытых обращений',
        'desired_date': day_params_and_analytics['mttr']['today']['number closed trouble tickets'],
        'comparison_date': day_params_and_analytics['mttr']['comparison day']['number closed trouble tickets']}
        )
    content.append(
        {'number': 22,
        'name': 'Общая нагрузка относительно нормы',
        'desired_date': day_params_and_analytics['mttr']['analytics']['load relative norm'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 23,
        'name': 'Общая нагрузка относительно дня сравнения',
        'desired_date': day_params_and_analytics['mttr']['analytics']['load relative comparison day'],
        'comparison_date': 'n/a'}
    )
    
    content.append(
        {'number': 24,
        'name': 'FLR',
        'desired_date': day_params_and_analytics['flr']['today']['flr'],
        'comparison_date': day_params_and_analytics['flr']['comparison day']['flr'],}
        )
    content.append(
        {'number': 25,
        'name': 'Общее количество первичных обращений',
        'desired_date': day_params_and_analytics['flr']['today']['number primary trouble tickets'],
        'comparison_date': day_params_and_analytics['flr']['comparison day']['number primary trouble tickets']}
        )
    content.append(
        {'number': 26,
        'name': 'Общee количество обращений закрытых без привлечения других отделов',
        'desired_date': day_params_and_analytics['flr']['today']['number trouble ticket closed independently'],
        'comparison_date': day_params_and_analytics['flr']['comparison day']['number trouble ticket closed independently']}
    )
    content.append(
        {'number': 27,
        'name': 'Общая нагрузка относительно нормы',
        'desired_date': day_params_and_analytics['flr']['analytics']['load relative norm'],
        'comparison_date': 'n/a'}
    )
    content.append(
        {'number': 28,
        'name': 'Общая нагрузка относительно дня сравнения',
        'desired_date': day_params_and_analytics['flr']['analytics']['load relative comparison day'],
        'comparison_date': 'n/a'}
    )
    return content