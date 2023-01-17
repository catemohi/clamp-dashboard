from django.contrib import admin
from django.urls import path, include

from .views import index, dashboard_json_data
from .views import dashboard, table, reports
from .views import table_json_data, report_json_data

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('table/', table, name='table'),
    path('reports/', reports, name='reports'),
    path('json/dashboard', dashboard_json_data, name='json/dashboard'),
    path('json/table', table_json_data, name='json/table'),
    path('json/reports', report_json_data, name='json/reports'),
]
