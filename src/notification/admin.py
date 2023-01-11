from django.contrib import admin

from .models import StepNotificationSetting, NotificationMessage
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

    list_display = ('time', 'subtype', 'text')
    list_display_links = ('time', 'subtype', 'text')
    search_fields = ('time', 'subtype', 'text')


admin.site.register(StepNotificationSetting, StepNotificationSettingAdmin)
admin.site.register(RetrunToWorkNotificationSetting,
                    RetrunToWorkNotificationSettingAdmin)
admin.site.register(NotificationMessage,
                    NotificationMessageAdmin)
