from django.contrib import admin

from .models import NaumenSetting, RatingSetting


class NaumenSettingAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class RatingSettingAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(NaumenSetting, NaumenSettingAdmin)
admin.site.register(RatingSetting, RatingSettingAdmin)
