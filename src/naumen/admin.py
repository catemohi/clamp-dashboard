from django.contrib import admin

from .models import FlrReport, MeanTimeToResponseReport, ServiceLevelReport
from .models import TroubleTicket
# Register your models here.


class ServiceLevelReportAdmin(admin.ModelAdmin):

    list_display = ('date', 'name_group', 'total_number_trouble_ticket',
                    'number_primary_trouble_tickets',
                    'number_of_trouble_ticket_taken_before_deadline',
                    'number_of_trouble_ticket_taken_after_deadline',
                    'service_level')
    list_display_links = ('date', 'name_group')
    search_fields = ('date', 'name_group', 'total_number_trouble_ticket',
                     'number_primary_trouble_tickets',
                     'number_of_trouble_ticket_taken_before_deadline',
                     'number_of_trouble_ticket_taken_after_deadline',
                     'service_level')


class MeanTimeToResponseReportAdmin(admin.ModelAdmin):

    list_display = ('date', 'total_number_trouble_ticket',
                    'average_mttr', 'average_mttr_tech_support')
    list_display_links = ('date',)
    search_fields = ('date', 'total_number_trouble_ticket',
                     'average_mttr', 'average_mttr_tech_support')


class FlrReportAdmin(admin.ModelAdmin):

    list_display = ('date', 'flr_level',
                    'number_trouble_ticket_closed_independently',
                    'number_primary_trouble_tickets')
    list_display_links = ('date',)
    search_fields = ('date', 'flr_level',
                     'number_trouble_ticket_closed_independently',
                     'number_primary_trouble_tickets')


class TroubleTicketAdmin(admin.ModelAdmin):

    list_display = ('number', 'name', 'last_edit_time', 'issue_type',
                    'name_contragent', 'vip_contragent', 'name_service',
                    'responsible', 'step', 'step_time')
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name_contragent', 'responsible', 'step',
                     'last_edit_time', 'step_time')


admin.site.register(TroubleTicket, TroubleTicketAdmin)
admin.site.register(ServiceLevelReport, ServiceLevelReportAdmin)
admin.site.register(MeanTimeToResponseReport, MeanTimeToResponseReportAdmin)
admin.site.register(FlrReport, FlrReportAdmin)
