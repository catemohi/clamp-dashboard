import os
import sys
from typing import Union, List
from functools import wraps
from threading import Thread
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import BotCommand
from telegram_bot.services import create_user, get_user_id, get_user_subscriptions
from telegram_bot.services import unsubscribe, subscribe, get_channels, get_ban_user
from telegram_bot.services import authorizate_user, ban_user, get_waited_user, get_admin
from telegram_bot.services import replace_for_markdown
from telegram_bot.services import get_sl, get_mttr, get_flr, get_aht
from telegram_bot import message_utils

# Объявление переменной бота
UPDATER = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
DISPATCHER = UPDATER.dispatcher


def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton,
                          List[InlineKeyboardButton]] = None,
    footer_buttons: Union[InlineKeyboardButton,
                          List[InlineKeyboardButton]] = None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list)
                    else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list)
                    else [footer_buttons])
    return menu


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id in get_ban_user():
            context.bot.send_sticker(update.effective_chat.id,
                                     message_utils.NO_PIKACHU)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=message_utils.BAN_MESSAGE)
            return
        if user_id not in get_user_id():
            context.bot.send_sticker(update.effective_chat.id,
                                     message_utils.NO_PIKACHU)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=message_utils.NOT_AUTH_MESSAGE)
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def admin_restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in get_admin():
            context.bot.send_sticker(update.effective_chat.id,
                                     message_utils.NO_PIKACHU)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=message_utils.NOT_ADMIN_MESSAGE)
            return
        return func(update, context, *args, **kwargs)
    return wrapped


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        UPDATER.start_polling()


def stop_and_restart():
    """Gracefully stop the Updater and
    replace the current process with a new one"""
    UPDATER.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


def start(update, context):

    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    if user_id not in get_user_id():
        text = message_utils.HELLO_MESSAGE_NEW.format(first_name)
    else:
        text = message_utils.HELLO_MESSAGE.format(first_name)
    text = replace_for_markdown(text)
    context.bot.send_sticker(update.effective_chat.id,
                             message_utils.HI_PIKACHU)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode='MarkdownV2')


@restricted
def restart(update, context):
    update.message.reply_sticker(message_utils.POKEBALL)
    update.message.reply_text(message_utils.RESTART_MESSAGE)
    Thread(target=stop_and_restart).start()
    update.message.reply_text("Я вновь тут!")


def register_user(update, context):
    """Регистрация пользователя

    Args:
        update (_type_): _description_
        context (_type_): _description_
    """
    user_id = str(update.message.from_user.id)
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username
    try:
        create_user(user_id, first_name, last_name, username)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message_utils.REGISTRATION_EXIST)
        return
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message_utils.REGISTRATION_SUCCESS)


@restricted
def user_subscriptions(update, context):
    """Регистрация пользователя

    Args:
        update (_type_): _description_
        context (_type_): _description_
    """
    user_id = str(update.message.from_user.id)
    try:
        user_subscriptions = get_user_subscriptions(user_id)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    if not user_subscriptions:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message_utils.NOT_SUBSCRIPTIONS_MESSAGE)
        return
    subscriptions_text = ""
    for num, subscription in enumerate(user_subscriptions, 1):
        subscriptions_text += "{}) *{}*\n".format(num, subscription[0])
    info_text = message_utils.YOUR_SUB.format(subscriptions_text)
    info_text = replace_for_markdown(info_text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=info_text, parse_mode='MarkdownV2')


@restricted
def unsubscribe_channel(update, context):
    """Регистрация пользователя

    Args:
        update (_type_): _description_
        context (_type_): _description_
    """
    user_id = str(update.message.from_user.id)
    try:
        user_subscriptions = get_user_subscriptions(user_id)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    if len(user_subscriptions) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message_utils.NOT_SUBSCRIPTIONS_MESSAGE)
        return

    button_list = [InlineKeyboardButton(channel[0],
                                        callback_data="%s_UNSUB" % channel[1])
                   for channel in user_subscriptions]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message_utils.CHOICE_SUB,
                             reply_markup=reply_markup,
                             parse_mode='MarkdownV2')


@restricted
def callback_unsubsctibe(update, context):
    query = update.callback_query
    data = query.data.replace('_UNSUB', '')
    user_id = str(query.from_user.id)
    try:
        unsubscribe(user_id, data)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    query.edit_message_text(text=message_utils.UNSCRIBE_SUCCESS_MESSAGE)


@restricted
def subscribe_channel(update, context):
    """Регистрация пользователя

    Args:
        update (_type_): _description_
        context (_type_): _description_
    """
    channels = get_channels()
    button_list = [InlineKeyboardButton(channel[0],
                                        callback_data="%s_SUB" % channel[2])
                   for channel in channels]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message_utils.CHOICE_CHANNEL,
                             reply_markup=reply_markup,
                             parse_mode='MarkdownV2')


@restricted
def callback_subsctibe(update, context):
    query = update.callback_query
    data = query.data.replace('_SUB', '')
    user_id = str(query.from_user.id)
    user_subscriptions = get_user_subscriptions(user_id)
    user_subscriptions = [sub[1] for sub in user_subscriptions]
    if data in user_subscriptions:
        query.edit_message_text(text=message_utils.SUBSCRIBE_EXIST)
        return
    try:
        subscribe(user_id, data)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    query.edit_message_text(text=message_utils.SUBSCRIBE_SUCCESS_MESSAGE)


@restricted
def get_notification_channel(update, context):
    """Регистрация пользователя

    Args:
        update (_type_): _description_
        context (_type_): _description_
    """
    try:
        channels = get_channels()
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    channels_text = ""
    for num, channel in enumerate(channels, 1):
        channels_text += message_utils.CHANNEL_TEXT.format(num, channel[0],
                                                           channel[1])
    text = message_utils.CHANNEL_HEAD.format(channels_text)
    text = replace_for_markdown(text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text, parse_mode='MarkdownV2')


@restricted
@admin_restricted
def auth_user(update, context):
    """Регистрация пользователя

    Args:
        update (_type_): _description_
        context (_type_): _description_
    """
    waited_users = get_waited_user()
    if len(waited_users) == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_utils.NOT_WAITED)
        return
    for user in waited_users:
        button_list = []
        name = message_utils.USER_FORM.format(user[1], user[2], user[0])
        button_list = [
            InlineKeyboardButton(message_utils.RUN_AUTH,
                                 callback_data="%s_AUTH" % user[0]),
            InlineKeyboardButton(message_utils.RUN_BAN,
                                 callback_data="%s_BAN" % user[0]),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=name, reply_markup=reply_markup)


@restricted
@admin_restricted
def callback_auth(update, context):
    query = update.callback_query
    data = query.data.replace('_AUTH', '')
    try:
        authorizate_user(data)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    query.edit_message_text(text=message_utils.USER_IS_AUTH.format(data))


@restricted
@admin_restricted
def callback_ban(update, context):
    query = update.callback_query
    data = query.data.replace('_BAN', '')
    try:
        ban_user(data)
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    query.edit_message_text(text=message_utils.USER_IS_BAN.format(data))


@restricted
def get_report(update, context):
    """Регистрация пользователя

    Args:
        update (_type_): _description_
        context (_type_): _description_
    """
    report_list = ('SL', 'MTTR', 'FLR', 'AHT')
    button_list = [InlineKeyboardButton(
        message_utils.EMOJI_REPORT + ' ' + report,
        callback_data="%s_REPORT" % report)
                   for report in report_list]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message_utils.CHOICE_REPORT,
                             reply_markup=reply_markup,
                             parse_mode='MarkdownV2')


@restricted
def callback_sl(update, context):
    query = update.callback_query
    try:
        text = get_sl()
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    message = message_utils.REPORT_HEAD.format(name="SL",
                                               time=datetime.strftime(
                                                   datetime.now(), "%d.%m.%Y"))
    message += text
    message = replace_for_markdown(message)
    query.edit_message_text(text=message, parse_mode='MarkdownV2')


@restricted
def callback_mttr(update, context):
    query = update.callback_query
    try:
        text = get_mttr()
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    message = message_utils.REPORT_HEAD.format(name="MTTR",
                                               time=datetime.strftime(
                                                   datetime.now(), "%d.%m.%Y"))
    message += text
    message = replace_for_markdown(message)
    query.edit_message_text(text=message, parse_mode='MarkdownV2')


@restricted
def callback_flr(update, context):
    query = update.callback_query
    try:
        text = get_flr()
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    message = message_utils.REPORT_HEAD.format(name="FLR",
                                               time=datetime.strftime(
                                                   datetime.now(), "%d.%m.%Y"))
    message += text
    message = replace_for_markdown(message)
    query.edit_message_text(text=message, parse_mode='MarkdownV2')


@restricted
def callback_aht(update, context):
    query = update.callback_query
    try:
        text = get_aht()
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))
        return
    message = message_utils.REPORT_HEAD.format(name="AHT",
                                               time=datetime.strftime(
                                                   datetime.now(), "%d.%m.%Y"))
    message += text
    message = replace_for_markdown(message)
    query.edit_message_text(text=message, parse_mode='MarkdownV2')


@restricted
def help(update, context):
    message = replace_for_markdown(message_utils.HELP_MESSAGE)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message, parse_mode='MarkdownV2')


DISPATCHER.add_handler(CommandHandler('start', start))
DISPATCHER.add_handler(CommandHandler('registration', register_user))
DISPATCHER.add_handler(CommandHandler('r', restart))
# DISPATCHER.add_handler(CallbackQueryHandler(button))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_subsctibe, pattern='^.*_SUB$'))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_unsubsctibe, pattern='^.*_UNSUB$'))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_auth, pattern='^.*_AUTH$'))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_ban, pattern='^.*_BAN$'))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_aht, pattern='^AHT_REPORT$'))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_sl, pattern='^SL_REPORT$'))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_flr, pattern='^FLR_REPORT$'))
DISPATCHER.add_handler(CallbackQueryHandler(
    callback_mttr, pattern='^MTTR_REPORT$'))
DISPATCHER.add_handler(CommandHandler('subscriptions', user_subscriptions))
DISPATCHER.add_handler(CommandHandler('help', help))
DISPATCHER.add_handler(CommandHandler('unsubscribe', unsubscribe_channel))
DISPATCHER.add_handler(CommandHandler('subscribe', subscribe_channel))
DISPATCHER.add_handler(CommandHandler('channels', get_notification_channel))
DISPATCHER.add_handler(CommandHandler('auth', auth_user))
DISPATCHER.add_handler(CommandHandler('report', get_report))
UPDATER.bot.set_my_commands([BotCommand('start', 'Начало работы с ботом'),
                             BotCommand('registration', 'Регистрация'),
                             BotCommand('report', 'Получить отчёт'),
                             BotCommand('subscriptions',
                                        'Показать список подписок'),
                             BotCommand('subscribe', 'Подписаться на канал'),
                             BotCommand('unsubscribe', 'Отписаться от канала'),
                             BotCommand('channels', 'Показать список каналов'),
                             BotCommand('auth', 'Авторизация пользователей'),
                             ])
