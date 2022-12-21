from django.contrib import admin

from .models import StepNotificationSetting


class StepNotificationSettingAdmin(admin.ModelAdmin):

    list_display = ('steps', 'step_time')
    list_display_links = ('steps', 'step_time')
    search_fields = ('steps', 'step_time')


admin.site.register(StepNotificationSetting, StepNotificationSettingAdmin)
