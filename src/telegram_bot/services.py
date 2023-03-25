from re import findall, sub
from json import dumps
from typing import Sequence, Literal, Union, Iterable, Mapping

from django.conf import settings
from requests import post

from .models import TelegramUser, NotificationChannel
from .message_utils import format_mttr_message, format_flt_message
from .message_utils import format_aht_message, format_sl_message

from dashboard import services as dashboard_services


def get_user_id() -> Sequence[str]:
    """Получить id пользователей.

    Returns:
        Sequence[str]: коллекция ID
    """
    return [int(user.tlgm_id) for user in
            TelegramUser.objects.filter(auth_status=True)]


def get_waited_user() -> Sequence[str]:
    """Получить пользователей которые ждут авторизации

    Returns:
        Sequence[str]: коллекция ID
    """
    return [(int(user.tlgm_id), user.tlgm_first_name, user.tlgm_username) for user in
            TelegramUser.objects.filter(auth_status=False, ban_status=False)]


def get_ban_user() -> Sequence[str]:
    """Получить пользователей которые ждут авторизации

    Returns:
        Sequence[str]: коллекция ID
    """
    return [int(user.tlgm_id) for user in
            TelegramUser.objects.filter(ban_status=True)]


def get_admin() -> Sequence[str]:
    """Получить пользователей которые ждут авторизации

    Returns:
        Sequence[str]: коллекция ID
    """
    return [int(user.tlgm_id) for user in
            TelegramUser.objects.filter(is_admin=True)]


def authorizate_user(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_
    """
    tlgm_user_queryset = TelegramUser.objects.filter(tlgm_id=user_id)
    if not tlgm_user_queryset.exists():
        raise ValueError("User with id '%s' not exists" % user_id)
    if len(tlgm_user_queryset) > 1:
        raise ValueError("User has more than one."
                         "Specify multiple arguments for search.")
    user = tlgm_user_queryset.first()
    user.auth_status = True
    user.save()


def ban_user(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_
    """
    tlgm_user_queryset = TelegramUser.objects.filter(tlgm_id=user_id)
    if tlgm_user_queryset.exists():
        raise ValueError("User with id '%s' already exists" % user_id)
    if len(tlgm_user_queryset) > 1:
        raise ValueError("User has more than one."
                         "Specify multiple arguments for search.")
    user = tlgm_user_queryset.first()
    user.auth_status = False
    user.ban_status = True
    user.subscriptions.clear()
    user.save()


def authorization_check(tlgm_id: str) -> bool:
    """Проверка авторизации пользователя

    Args:
        tlgm_id (str): Telegram ID пользователя

    Returns:
        bool: результат проверки
    """
    tlgm_user_queryset = TelegramUser.objects.filter(tlgm_id=tlgm_id)
    if not tlgm_user_queryset.exists():
        return False
    user = tlgm_user_queryset.first()
    if user is None:
        return False
    return user.auth_status


def create_user(user_id: str, first_name: str = '',
                last_name: str = '', username: str = '') -> None:
    """Создание нового пользователя
    """
    tlgm_user_queryset = TelegramUser.objects.filter(tlgm_id=user_id)
    if tlgm_user_queryset.exists():
        raise ValueError("User with id '%s' already exists" % user_id)
    TelegramUser.objects.create(tlgm_id=user_id, tlgm_first_name=first_name,
                                tlgm_last_name=last_name,
                                tlgm_username=username)


def delete_user(user_id: str = None, first_name: str = None,
                last_name: str = None, username: str = None) -> None:
    """Удаление пользователя
    """
    user_filter = {}
    if user_id is not None:
        user_filter["tlgm_id"] = user_id
    if first_name is not None:
        user_filter["tlgm_first_name"] = first_name
    if last_name is not None:
        user_filter["tlgm_last_name"] = last_name
    if username is not None:
        user_filter["tlgm_username"] = username
    if not user_filter:
        raise ValueError("Arguments must be specified and not equals NONE")
    tlgm_user_queryset = TelegramUser.objects.filter(**user_filter)
    if not tlgm_user_queryset.exists():
        raise ValueError("User not exists")
    if len(tlgm_user_queryset) > 1:
        raise ValueError("User has more than one."
                         "Specify multiple arguments for search.")
    user = tlgm_user_queryset.first()
    user.delete()


def get_channels() -> Sequence[str]:
    """Получить каналы на которые можно подписаться.

    Returns:
        Sequence[str]: коллекция каналов
    """
    return [(channel.human_name, channel.description, channel.name) for channel
            in NotificationChannel.objects.all()]


def subscribe(user_id: str, channel_name: str) -> bool:
    """_summary_

    Args:
        user_id (_type_): _description_
        channel_name (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        bool: _description_
    """
    tlgm_user_queryset = TelegramUser.objects.filter(tlgm_id=user_id)
    if not tlgm_user_queryset.exists():
        raise ValueError("User %s not exists" % user_id)
    if len(tlgm_user_queryset) > 1:
        raise ValueError("User %s has more than one" % user_id)
    channel_queryset = NotificationChannel.objects.filter(name=channel_name)
    if not channel_queryset.exists():
        raise ValueError("Channel %s not exists" % channel_name)
    if len(channel_queryset) > 1:
        raise ValueError("Channel %s has more than one" % channel_name)

    channel = channel_queryset.first()
    user = tlgm_user_queryset.first()
    user.subscriptions.add(channel)
    return True


def unsubscribe(user_id: str, channel_name: str) -> bool:
    """_summary_

    Args:
        user_id (_type_): _description_
        channel_name (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        bool: _description_
    """
    tlgm_user_queryset = TelegramUser.objects.filter(tlgm_id=user_id)
    if not tlgm_user_queryset.exists():
        raise ValueError("User %s not exists" % user_id)
    if len(tlgm_user_queryset) > 1:
        raise ValueError("User %s has more than one" % user_id)
    channel_queryset = NotificationChannel.objects.filter(name=channel_name)
    if not channel_queryset.exists():
        raise ValueError("Channel %s not exists" % channel_name)
    if len(channel_queryset) > 1:
        raise ValueError("Channel %s has more than one" % channel_name)

    channel = channel_queryset.first()
    user = tlgm_user_queryset.first()
    user.subscriptions.remove(channel)
    return True


def get_user_subscriptions(user_id: str) -> Sequence[str]:
    """_summary_

    Args:
        user_id (_type_): _description_
        channel_name (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        bool: _description_
    """
    tlgm_user_queryset = TelegramUser.objects.filter(tlgm_id=user_id)
    if not tlgm_user_queryset.exists():
        raise ValueError("User %s not exists" % user_id)
    if len(tlgm_user_queryset) > 1:
        raise ValueError("User %s has more than one" % user_id)

    user = tlgm_user_queryset.first()
    subscriptions_queryset = user.subscriptions.all()
    return [(channel.human_name, channel.name)
            for channel in subscriptions_queryset]


def replace_for_markdown(data: str) -> str:
    """Функция экранирует знаки, которые требует экранирование
    при использовании стиля текста "markdownV2".

    Args:
        data (str): сырой текст

    Returns:
        str: экранированный текст
    """
    pattern = r'[-.+?^$[\](){}><!]'
    list_after = []
    for line in data.split('\n'):
        if 'http' in line:
            list_after.append(line)
            continue
        elif 'tg://' in line:
            list_after.append(line)
            continue
        words = findall(pattern, line)
        if words:
            for word in words:
                local_patern = rf'[{word}]'
                escaped_word = '\\' + word
                if escaped_word in line:
                    continue
                line = sub(local_patern, escaped_word, line)
        list_after.append(line)

    return '\n'.join(list_after)


def send_telegram_content(
    content: str,
    method: Literal['text', 'gif', 'sticker'] = 'text',
    chat_ids: Sequence[Union[str, int]] = [],
    token: str = settings.TELEGRAM_TOKEN,
    api_uri: str = 'api.telegram.org'
) -> None:
    """Функция для отправки контента от бота через api.
    На вход получает метод, id чата, куда отправлять и сам контент.
    Функция хранит в себе методы, в виде словаря

    Args:
        content (str): данные которые необходимо отправить
        method (Literal[text, gif, sticker], optional): метод API.
        По умолчанию 'text'.
        chat_ids (Sequence[Union[str, int]], optional): ID получателей.
        По умолчанию [].
        token (str, optional): токен бота.
        По умолчанию settings.TELEGRAM_TOKEN.
        api_uri (str, optional): ссылка API.
        По умолчанию 'api.telegram.org'.
    """
    if method not in ['text', 'gif', 'sticker']:
        raise ValueError('Method must be ["text", "gif", "sticker"]')
    if not chat_ids:
        return
    if not token:
        raise ValueError('Token must be specified')
    if not content:
        raise ValueError('Content must be specified')
    if not api_uri:
        raise ValueError('API URI must be specified')
    dict_methods = {
        'gif': ['sendAnimation', 'animation'],
        'sticker': ['sendSticker', 'sticker'],
        'text': ['sendMessage', 'text']
        }
    url_format = "{proto}://{api}/bot{token}/{method}"
    url = url_format.format(proto='https', api=api_uri,
                            token=token,
                            method=dict_methods[method][0])
    if method == 'text':
        if not isinstance(content, str):
            raise ValueError('Content for method %s must be a string' % method)
        content = replace_for_markdown(content)

    for chat_id in chat_ids:
        data = {'parse_mode': 'MarkdownV2'}
        data.update({'chat_id': str(chat_id)})
        data.update({dict_methods[method][1]: content})
        responce = post(url, data)
        if not responce:
            raise Exception('Error push POST request to %s' % api_uri)


def send_message_to_channel(message: str, channel: str) -> Iterable:
    """Отправка уведомления всем подписчикам канала.

    Args:
        message (str): текст сообщения
        channel (str): имя канала

    Returns:
        Iterable[bool, str]: статус отправки, сообщение
    """
    channel_queryset = NotificationChannel.objects.filter(name=channel)
    if not channel_queryset.exists():
        return (False, "Channel not found")
    if len(channel_queryset) > 1:
        return (False, "Channel too many")
    channel = channel_queryset.first()
    chat_ids = channel.get_id_subscribers()
    try:
        send_telegram_content(message, 'text', chat_ids)
    except ValueError as e:
        return (False, str(e))
    except Exception as e:
        return (False, str(e))
    return (True, "OK")


def push_to_telegram(notification: Mapping) -> None:
    """_summary_

    Args:
        notification (Mapping): _description_
    """
    print(dumps(notification))
    text = notification.get('text', '')
    send_message_to_channel(text, "reports")


def get_sl() -> str:
    """Получени отчета SL и отправка его в telegram

    Returns:
        str: отформотированное сообщение
    """
    # day = get_day_dates_and_data().get("dashboard_data", {})
    # text = format_sl_message(day)
    text = ""
    return text


def get_mttr() -> str:
    """Получени отчета MTTR и отправка его в telegram

    Returns:
        str: отформотированное сообщение
    """
    # day = get_day_dates_and_data()
    # text = format_mttr_message(day)
    text = ""
    return text


def get_flr() -> str:
    """Получени отчета FLR и отправка его в telegram

    Returns:
        str: отформотированное сообщение
    """
    # day = get_day_dates_and_data()
    # text = format_flt_message(day)
    text = ""
    return text


def get_aht() -> str:
    """Получени отчета AHT и отправка его в telegram

    Returns:
        str: отформотированное сообщение
    """
    # day = get_day_dates_and_data()
    # text = format_aht_message(day)
    text = ""
    return text
