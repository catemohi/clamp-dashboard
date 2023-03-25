from typing import Mapping

from dashboard import services


# EMOJI
EMOJI_RED_CROSS = "\U0000274C"
EMOJI_GREEN_CHECK = "\U00002705"
EMOJI_REPORT = "\U0001F4CA"
EMOJI_RED_CIRCLE = "\U0001F534"
EMOJI_GREEN_CIRCLE = "\U0001F7E2"
# MESSAGE
NOT_SUBSCRIPTIONS_MESSAGE = EMOJI_RED_CROSS + " У вас нет активных подписок!"
REGISTRATION_EXIST = EMOJI_RED_CROSS + " Вы уже зарегистрированы!"
SUBSCRIBE_EXIST = EMOJI_RED_CROSS + " Вы уже подписаны на этот канал!"
NOT_ADMIN_MESSAGE = EMOJI_RED_CROSS + " Вы не администратор!"
NOT_AUTH_MESSAGE = EMOJI_RED_CROSS + " Вы не авторизированы!"
BAN_MESSAGE = EMOJI_RED_CROSS + " Вы не заблокированы!"
SUBSCRIBE_SUCCESS_MESSAGE = EMOJI_GREEN_CHECK \
    + " Вы успешно подписаны на канал!"
UNSCRIBE_SUCCESS_MESSAGE = EMOJI_GREEN_CHECK + " Подписка на канал прекращена."
REGISTRATION_SUCCESS = EMOJI_GREEN_CHECK + " Вы зарегистрированы!\n" +\
    "Подождите пока администратор, авторизует вас."
REPORT_HEAD = EMOJI_REPORT + " Отчёт {name} за {time}\n"
HELLO_MESSAGE_NEW = "Привет, {}!\n" +\
    "Для использования бота требуеться регистрация.\n" +\
    "Отправьте, пожалуйста, команду /registration " +\
    "и дождитесь авторизации."
HELLO_MESSAGE = "Привет, {}\n" +\
    "Для вывода команд набери: /help"
RESTART_MESSAGE = 'Бот перезапускаеться...'
CHOICE_SUB = "*Выберете подписку*:"
YOUR_SUB = 'Вы подписаны на каналы:\n{}'
CHOICE_CHANNEL = "*Выберете канал*:"
CHANNEL_TEXT = "{}) *{}*\nОписание: {}\n\n"
CHANNEL_HEAD = "Для подписки доступны каналы:\n\n{}"
CHOICE_REPORT = "*Выберете интересующий отчет*:"
USER_IS_BAN = "Пользователь с ID {} заблокирован."
USER_IS_AUTH = "Пользователь с ID {} авторизован."
NOT_WAITED = EMOJI_RED_CROSS + " Нет пользователей ожидающих авторизации!"
USER_FORM = "Имя: {}\nНик: @{}\nID: {}"
RUN_AUTH = EMOJI_GREEN_CHECK + " Авторизовать"
RUN_BAN = EMOJI_RED_CROSS + " Заблокировать"
# HELP MESSAGE
HELP_MESSAGE = (
    "*Команды бота:*\n\n"
    "*/start* — начало работы с ботом\n"
    "*/registration* — регистрация в боте\n"
    "*/report* — получение отчётов тех.по за день\n"
    "*/subscriptions* — показать список ваших подписок\n"
    "*/channels* — показать список каналов уведомлений\n"
    "*/subscribe* — подписаться на канал уведомлений\n"
    "*/unsubscribe* — отписаться от канала уведомлений\n"
    "*/auth* — авторизация пользователей в боте\n"
)
# STICKER
HI_PIKACHU = "CAACAgIAAxkBAAEIRm5kHbxOLFBHpWJwNWybL" +\
    "GCvA1g50AACWQADIfAEHEef7qP9uC3xLwQ"
NO_PIKACHU = "CAACAgIAAxkBAAEIRrRkHdaqdVZ4K_" +\
    "fjRgwZkhMH81khvQACPwADIfAEHCvrDhu9ZzKqLwQ"
WALKING_PIKACHE = "CAACAgIAAxkBAAEISmBkHe8D25o1aDdEDODis" +\
    "J7gUvs2ogACNwADIfAEHDSxG1UoZ4a8LwQ"
POKEBALL = "CAACAgIAAxkBAAEIS4dkHfbJGBkFlb3pV" +\
    "rydJ2cp9o5SiAACqSEAAosY0UhpT6noUQv9ni8E"
HAGS = "CAACAgIAAxkBAAEIS5NkHfjogG8nbW2f3Efwd" +\
    "1v8p9PJFgAChRsAAjLHwUjJM1wXg4u6Fy8E"
# FORMAT MESSAGES


def format_sl_message(data: Mapping) -> str:
    """Форматированние данных под отчет SL

    Args:
        data (Mapping): данные для форматирования

    Returns:
        str: форматированная строка данных
    """
    ratings = services.get_load_ratings()
    first_line_analytics = data.get('analytics', {}).get('sl', {}).get('first_line', {})
    first_line = data.get('sl', {}).get('first_line', {})
    first_line_num_issues = first_line.num_issues if first_line else 0
    first_line_num_worked_before_deadline = first_line.num_worked_before_deadline if first_line else 0
    first_line_num_worked_after_deadline = first_line.num_worked_after_deadline if first_line else 0
    first_line_rating_to_nominal = first_line_analytics.rating_to_nominal if first_line_analytics else 0
    first_line_rating_to_nominal = "> на {}%".format(abs(int(first_line_rating_to_nominal))) if int(first_line_rating_to_nominal) >= 0 else "< на {}%".format(abs(int(first_line_rating_to_nominal)))
    first_line_dayly_sl = first_line.dayly_sl if first_line else 0
    first_line_emoji_sl = EMOJI_GREEN_CIRCLE if int(first_line_dayly_sl) >= ratings.service_level else EMOJI_RED_CIRCLE
    first_line_weekly_sl = first_line.weekly_sl if first_line else 0
    first_line_mountly_sl = first_line.mountly_sl if first_line else 0

    vip_line_analytics = data.get('analytics', {}).get('sl', {}).get('vip_line', {})
    vip_line = data.get('sl', {}).get('vip_line', {})
    vip_line_num_issues = vip_line.num_issues if vip_line else 0
    vip_line_num_worked_before_deadline = vip_line.num_worked_before_deadline if vip_line else 0
    vip_line_num_worked_after_deadline = vip_line.num_worked_after_deadline if vip_line else 0
    vip_line_rating_to_nominal = vip_line_analytics.rating_to_nominal if vip_line_analytics else 0
    vip_line_rating_to_nominal = "> на {}%".format(abs(int(vip_line_rating_to_nominal))) if int(vip_line_rating_to_nominal) >= 0 else "< на {}%".format(abs(int(vip_line_rating_to_nominal)))
    vip_line_dayly_sl = vip_line.dayly_sl if vip_line else 0
    vip_line_emoji_sl = EMOJI_GREEN_CIRCLE if int(vip_line_dayly_sl) >= ratings.service_level else EMOJI_RED_CIRCLE
    vip_line_weekly_sl = vip_line.weekly_sl if vip_line else 0
    vip_line_mountly_sl = vip_line.mountly_sl if vip_line else 0

    general_analytics = data.get('analytics', {}).get('sl', {}).get('general', {})
    general = data.get('sl', {}).get('general', {})
    general_num_issues = general.num_issues if general else 0
    general_num_worked_before_deadline = general.num_worked_before_deadline if general else 0
    general_num_worked_after_deadline = general.num_worked_after_deadline if general else 0
    general_rating_to_nominal = general_analytics.rating_to_nominal if general_analytics else 0
    general_rating_to_nominal = "> на {}%".format(abs(int(general_rating_to_nominal))) if int(general_rating_to_nominal) >= 0 else "< на {}%".format(abs(int(general_rating_to_nominal)))
    general_dayly_sl = general.dayly_sl if general else 0
    general_dayly_emoji_sl = EMOJI_GREEN_CIRCLE if int(general_dayly_sl) >= ratings.service_level else EMOJI_RED_CIRCLE
    general_weekly_sl = general.weekly_sl if general else 0
    general_weekly_emoji_sl = EMOJI_GREEN_CIRCLE if int(general_weekly_sl) >= ratings.service_level else EMOJI_RED_CIRCLE
    general_mountly_sl = general.mountly_sl if general else 0
    general_mountly_emoji_sl = EMOJI_GREEN_CIRCLE if int(general_mountly_sl) >= ratings.service_level else EMOJI_RED_CIRCLE

    message = '=========\n' + \
        'Кол-во обращений за день на westcall линию: {}\n'\
        .format(first_line_num_issues) + \
        'Кол-во обращений westcall линии принятых вовремя: {}\n'\
        .format(first_line_num_worked_before_deadline) + \
        'Кол-во обращений westcall линии принятых после срока: {}\n'\
        .format(first_line_num_worked_after_deadline) + \
        'Нагрузка westcall линии относительно нормы: {}\n'\
        .format(first_line_rating_to_nominal) + \
        '{} Service Level westcall линии: {}%\n'.format(first_line_emoji_sl, first_line_dayly_sl) + \
        '=========\n' + \
        'Кол-во обращений за день на vip линию: {}\n'\
        .format(vip_line_num_issues) + \
        'Кол-во обращений vip линии принятых вовремя: {}\n'\
        .format(vip_line_num_worked_before_deadline) + \
        'Кол-во обращений vip линии принятых после срока: {}\n'\
        .format(vip_line_num_worked_after_deadline) + \
        'Нагрузка vip линии относительно нормы: {}\n'\
        .format(vip_line_rating_to_nominal) + \
        '{} Service Level vip линии: {}%\n'.format(vip_line_emoji_sl, vip_line_dayly_sl) + \
        '=========\n' + \
        'Общее кол-во обращений за день: {}\n'\
        .format(general_num_issues) + \
        'Общее Кол-во обращений принятых вовремя: {}\n'\
        .format(general_num_worked_before_deadline) + \
        'Общее кол-во обращений принятых после срока: {}\n'\
        .format(general_num_worked_after_deadline) + \
        'Общая нагрузка относительно нормы: {}\n'\
        .format(general_rating_to_nominal) + \
        '=========\n' + \
        '{} Общий дневной Service Level: {}%\n'.format(general_dayly_emoji_sl, general_dayly_sl) + \
        '{} Общий недельный Service Level: {}%\n'.format(general_weekly_emoji_sl, general_weekly_sl) + \
        '{} Общий месячный Service Level: {}%\n'.format(general_mountly_emoji_sl, general_mountly_sl) + \
        '=========\n'

    return message


def format_mttr_message(data: Mapping) -> str:
    """Форматированние данных под отчет MTTR

    Args:
        data (Mapping): данные для форматирования

    Returns:
        str: форматированная строка данных
    """
    ratings = services.get_load_ratings()
    mttr_analytics = data.get('analytics', {}).get('mttr', {})
    mttr = data.get('mttr', {})
    average_mttr_tech_support = mttr.average_mttr_tech_support if mttr else 0
    average_mttr_emoji_sl = EMOJI_GREEN_CIRCLE if int(average_mttr_tech_support) <= ratings.mttr_level else EMOJI_RED_CIRCLE
    weekly_average_mttr_tech_support = mttr.weekly_average_mttr_tech_support if mttr else 0
    weekly_average_mttr_emoji_sl = EMOJI_GREEN_CIRCLE if int(weekly_average_mttr_tech_support) <= ratings.mttr_level else EMOJI_RED_CIRCLE
    mountly_average_mttr_tech_support = mttr.mountly_average_mttr_tech_support if mttr else 0
    mountly_average_mttr_emoji_sl = EMOJI_GREEN_CIRCLE if int(mountly_average_mttr_tech_support) <= ratings.mttr_level else EMOJI_RED_CIRCLE
    num_issues = mttr.num_issues if mttr else 0
    rating_to_nominal = mttr_analytics.rating_to_nominal if mttr_analytics else 0
    rating_to_nominal = "> на {}%".format(abs(int(rating_to_nominal))) if int(rating_to_nominal) >= 0 else "< на {}%".format(abs(int(rating_to_nominal)))

    message = '=========\n' + \
        '{} Дневной MTTR: {} мин.\n'\
        .format(average_mttr_emoji_sl, average_mttr_tech_support) + \
        '{} Недельный MTTR: {} мин.\n'\
        .format(weekly_average_mttr_emoji_sl, weekly_average_mttr_tech_support) + \
        '{} Месячный MTTR: {} мин.\n'\
        .format(mountly_average_mttr_emoji_sl, mountly_average_mttr_tech_support) + \
        'Общее кол-во закрытых обращений: {}\n'\
        .format(num_issues) + \
        'Общая нагрузка относительно нормы: {}\n'\
        .format(rating_to_nominal) + \
        '=========\n'
    return message


def format_flt_message(data: Mapping) -> str:
    """Форматированние данных под отчет FLR

    Args:
        data (Mapping): данные для форматирования

    Returns:
        str: форматированная строка данных
    """
    ratings = services.get_load_ratings()
    flr_analytics = data.get('analytics', {}).get('flr', {})
    flr = data.get('flr', {})
    level = flr.level if flr else 0
    level_emoji_sl = EMOJI_GREEN_CIRCLE if int(level) >= ratings.flr_level else EMOJI_RED_CIRCLE
    weekly_level = flr.weekly_level if flr else 0
    weekly_level_emoji_sl = EMOJI_GREEN_CIRCLE if int(weekly_level) >= ratings.flr_level else EMOJI_RED_CIRCLE
    mountly_level = flr.mountly_level if flr else 0
    mountly_level_emoji_sl = EMOJI_GREEN_CIRCLE if int(mountly_level) >= ratings.flr_level else EMOJI_RED_CIRCLE
    num_primary_issues = flr.num_primary_issues if flr else 0
    num_issues_closed_independently = flr.num_issues_closed_independently if flr else 0
    rating_to_nominal = flr_analytics.rating_to_nominal if flr_analytics else 0
    rating_to_nominal = "> на {}%".format(abs(int(rating_to_nominal))) if int(rating_to_nominal) >= 0 else "< на {}%".format(abs(int(rating_to_nominal)))

    message = '=========\n' + \
        '{} Дневной FLR: {}%\n'\
        .format(level_emoji_sl, level) + \
        '{} Недельный FLR: {}%\n'\
        .format(weekly_level_emoji_sl, weekly_level) + \
        '{} Месячный FLR: {}%\n'\
        .format(mountly_level_emoji_sl, mountly_level) + \
        'Общее кол-во первичных обращений: {}\n'\
        .format(num_primary_issues) + \
        'Кол-во обращений закрытых самостоятельно: {}\n'\
        .format(num_issues_closed_independently) + \
        'Общая нагрузка относительно нормы: {}\n'\
        .format(rating_to_nominal) + \
        '=========\n'
    return message


def format_aht_message(data: Mapping) -> str:
    """Форматированние данных под отчет AHT

    Args:
        data (Mapping): данные для форматирования

    Returns:
        str: форматированная строка данных
    """
    ratings = services.get_load_ratings()
    aht_analytics = data.get('analytics', {}).get('aht', {})
    aht = data.get('aht', {})
    dayly_aht = aht.dayly_aht if aht else 0
    dayly_aht_sl = EMOJI_GREEN_CIRCLE if int(dayly_aht) <= ratings.aht_level else EMOJI_RED_CIRCLE
    weekly_aht = aht.weekly_aht if aht else 0
    weekly_aht_sl = EMOJI_GREEN_CIRCLE if int(weekly_aht) <= ratings.aht_level else EMOJI_RED_CIRCLE
    mountly_aht = aht.mountly_aht if aht else 0
    mountly_aht_sl = EMOJI_GREEN_CIRCLE if int(mountly_aht) <= ratings.aht_level else EMOJI_RED_CIRCLE
    issues_received = aht.issues_received if aht else 0
    rating_to_nominal = aht_analytics.rating_to_nominal if aht_analytics else 0
    rating_to_nominal = "> на {}%".format(abs(int(rating_to_nominal))) if int(rating_to_nominal) >= 0 else "< на {}%".format(abs(int(rating_to_nominal)))

    message = '=========\n' + \
        '{} Дневной AHT: {} мин.\n'\
        .format(dayly_aht_sl, dayly_aht) + \
        '{} Недельный AHT: {} мин.\n'\
        .format(weekly_aht_sl, weekly_aht) + \
        '{} Месячный AHT: {} мин.\n'\
        .format(mountly_aht_sl, mountly_aht) + \
        'Поступило обращений: {}\n'\
        .format(issues_received) + \
        'Общая нагрузка относительно нормы: {}\n'\
        .format(rating_to_nominal) + \
        '=========\n'
    return message
