from django.contrib import admin
from django.urls import path, include

from .views import index_page, login_page, logout_page
from .views import dashboard_page, table_page, reports_page
from .views import dashboard_json, table_json, report_json


urlpatterns = [
    path('', index_page, name='index'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('table/', table_page, name='table'),
    path('reports/', reports_page, name='reports'),
    path('json/dashboard', dashboard_json, name='json/dashboard'),
    path('json/table', table_json, name='json/table'),
    path('json/reports', report_json, name='json/reports'),
    ]


