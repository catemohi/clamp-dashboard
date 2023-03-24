from django.db import models
from typing import Sequence


class NotificationChannel(models.Model):
    """Модель хранящая каналы уведомлений
    """
    name = models.CharField(max_length=128, verbose_name="Название для ссылок")
    human_name = models.CharField(max_length=128,
                                  verbose_name="Отображаемое название",
                                  default='')
    description = models.TextField(verbose_name="Описание", default='',
                                   null=True, blank=True)
    # subscriber_users многие ко многим с TelegramUser
    # subscriber_chats многие ко многим с GroupChat

    def __str__(self) -> str:
        return self.name

    def get_id_subscribers(self) -> Sequence[str]:
        """Возвращает ID подписчиков на канал

        Returns:
            Sequence[str]: ID подписчиков
        """
        subscribers = []
        subscribers += [subscriber.tlgm_id for subscriber
                        in self.subscriber_users.all()]
        subscribers += [subscriber.tlgm_id for subscriber
                        in self.subscriber_chats.all()]
        return subscribers


class TelegramUser(models.Model):
    """Модель хранящая данные о пользователях бота
    """
    # Данные из модели telegram
    tlgm_id = models.CharField(primary_key=True, max_length=64,
                               verbose_name="Telegram ID")
    tlgm_first_name = models.CharField(max_length=32, null=True, blank=True,
                                       verbose_name="Telegram имя")
    tlgm_last_name = models.CharField(max_length=32, null=True, blank=True,
                                      verbose_name="Telegram фамилия")
    tlgm_username = models.CharField(max_length=32, null=True, blank=True,
                                     verbose_name="Telegram ник")
    # Данные авторизации пользователя
    auth_status = models.BooleanField(default=False,
                                      verbose_name="Авторизация")
    ban_status = models.BooleanField(default=False,
                                     verbose_name="Заблокирован")
    is_admin = models.BooleanField(default=False,
                                   verbose_name="Права администратора")
    # Подписки
    subscriptions = models.ManyToManyField(NotificationChannel,
                                           related_name="subscriber_users",
                                           null=True, blank=True)

    def __str__(self) -> str:
        return "({fn};@{username};{id})".format(fn=self.tlgm_first_name,
                                                username=self.tlgm_username,
                                                id=self.tlgm_id)


class GroupChat(models.Model):
    """Модель хранящая групповые чаты
    """
    name = models.CharField(max_length=128, verbose_name="Название")
    # Данные из модели telegram
    tlgm_id = models.CharField(primary_key=True, max_length=64,
                               verbose_name="Telegram ID")
    # Подписки
    subscriptions = models.ManyToManyField(NotificationChannel,
                                           related_name="subscriber_chats",
                                           null=True, blank=True)

    def __str__(self) -> str:
        return "{name}({id})".format(name=self.name,
                                     id=self.tlgm_id)
