from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import NaumenSetting, RatingSetting, Profile


class NaumenSettingAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class RatingSettingAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)

admin.site.register(NaumenSetting, NaumenSettingAdmin)
admin.site.register(RatingSetting, RatingSettingAdmin)
admin.site.register(User, CustomUserAdmin)
