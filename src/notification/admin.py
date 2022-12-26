from django.contrib import admin

from .models import StepNotificationSetting
from .models import RetrunToWorkNotificationSetting


class StepNotificationSettingAdmin(admin.ModelAdmin):

    list_display = ('name', 'step', 'step_time', 'alarm_time')
    list_display_links = ('name', 'step', 'step_time', 'alarm_time')
    search_fields = ('name', 'step', 'step_time', 'alarm_time')


class RetrunToWorkNotificationSettingAdmin(admin.ModelAdmin):

    list_display = ('name', 'step', 'alarm_time')
    list_display_links = ('name', 'step', 'alarm_time')
    search_fields = ('name', 'step', 'alarm_time')


class NotificationMessageAdmin(admin.ModelAdmin):

    list_display = ('datetime', 'text')
    list_display_links = ('datetime', 'text')
    search_fields = ('datetime', 'text')


admin.site.register(StepNotificationSetting, StepNotificationSettingAdmin)
admin.site.register(RetrunToWorkNotificationSetting, NotificationMessageAdmin,
                    RetrunToWorkNotificationSettingAdmin)
