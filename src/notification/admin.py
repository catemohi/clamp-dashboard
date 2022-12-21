from django.contrib import admin

from .models import StepNotificationSetting
from .models import RetrunToWorkNotificationSetting


class StepNotificationSettingAdmin(admin.ModelAdmin):

    list_display = ('step', 'step_time')
    list_display_links = ('step', 'step_time')
    search_fields = ('step', 'step_time')


class RetrunToWorkNotificationSettingAdmin(admin.ModelAdmin):

    list_display = ('step', 'step_time')
    list_display_links = ('step', 'step_time')
    search_fields = ('step', 'step_time')


admin.site.register(StepNotificationSetting, StepNotificationSettingAdmin)
admin.site.register(RetrunToWorkNotificationSetting,
                    RetrunToWorkNotificationSettingAdmin)
