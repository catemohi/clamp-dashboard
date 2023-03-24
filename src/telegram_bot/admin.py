from django.contrib import admin
from typing import Sequence
from .models import TelegramUser, NotificationChannel, GroupChat


class TelegramUserAdmin(admin.ModelAdmin):

    def user_subscriptions(self, object: TelegramUser) -> Sequence[str]:
        """Отображение многие ко многим поля

        Args:
            object (TelegramUser): модель пользователя

        Returns:
            Sequence[str]: подписки пользователя
        """
        return [channel.name for channel in object.subscriptions.all()]

    user_subscriptions.short_description = "Подписки"

    list_display = ('tlgm_id', 'tlgm_username', 'tlgm_first_name',
                    'tlgm_last_name', 'auth_status', 'is_admin',
                    'user_subscriptions')
    list_display_links = ('tlgm_id', 'tlgm_username')
    search_fields = ('tlgm_id', 'tlgm_username', 'auth_status',)


class NotificationChannelAdmin(admin.ModelAdmin):

    def subscribers(self, object: NotificationChannel) -> Sequence[str]:
        """Отображение многие ко многим поля

        Args:
            object (NotificationChannel): модель канала

        Returns:
            Sequence[str]: подписчики канала
        """
        subscribers = []
        subscribers += [str(user) for user in object.subscriber_users.all()]
        subscribers += [str(chat) for chat in object.subscriber_chats.all()]
        return subscribers

    subscribers.short_description = "Подписчики"

    list_display = ('name', 'subscribers')
    list_display_links = ('name',)
    search_fields = ('name',)


class GroupChatAdmin(admin.ModelAdmin):

    def group_subscriptions(self, object: GroupChat) -> Sequence[str]:
        """Отображение многие ко многим поля

        Args:
            object (GroupChat): модель чата

        Returns:
            Sequence[str]: подписки чата
        """
        return [channel.name for channel in object.subscriptions.all()]

    group_subscriptions.short_description = "Подписки"

    list_display = ('name', 'tlgm_id', 'group_subscriptions')
    list_display_links = ('name', 'tlgm_id')
    search_fields = ('name', 'tlgm_id')


admin.site.register(GroupChat, GroupChatAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(NotificationChannel, NotificationChannelAdmin)
