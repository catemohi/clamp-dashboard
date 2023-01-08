"""
Файл настроек Celery
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
from __future__ import absolute_import
import os
from json import dumps


from celery import Celery
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# этот код скопирован с manage.py
# он установит модуль настроек по умолчанию Django для приложения 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamp.settings')

# здесь вы меняете имя
app = Celery("clamp")

# Для получения настроек Django, связываем префикс "CELERY" с настройкой celery
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Moscow'
app.conf.task_routes = {
    'naumen.tasks.*': {'queue': 'naumen_crud'},
    'naumen.tasks.crud_issue': {'queue': 'celery'},
    'naumen.tasks.check_issue_deadline_and_timer': {'queue': 'celery'},
    'naumen.tasks.check_issues_deadline_and_timer': {'queue': 'celery'},
    }
# загрузка tasks.py в приложение django
app.autodiscover_tasks()
# создание необходимых периодов
thirty_seconds_schedule, created = IntervalSchedule.objects.get_or_create(
    every=30, period=IntervalSchedule.SECONDS)
minute_schedule, created = IntervalSchedule.objects.get_or_create(
    every=60, period=IntervalSchedule.SECONDS)
two_minutes_schedule, created = IntervalSchedule.objects.get_or_create(
    every=120, period=IntervalSchedule.SECONDS)
ten_minutes_schedule, created = IntervalSchedule.objects.get_or_create(
    every=10, period=IntervalSchedule.MINUTES)
fifteen_minutes_schedule, created = IntervalSchedule.objects.get_or_create(
    every=15, period=IntervalSchedule.MINUTES)
thirty_minutes_schedule, created = IntervalSchedule.objects.get_or_create(
    every=30, period=IntervalSchedule.MINUTES)
hour_schedule, created = IntervalSchedule.objects.get_or_create(
    every=60, period=IntervalSchedule.MINUTES)
six_hours_schedule, created = IntervalSchedule.objects.get_or_create(
    every=6, period=IntervalSchedule.HOURS)
# Создание переодических задач
PeriodicTask.objects.get_or_create(interval=fifteen_minutes_schedule,
                                   name='Обновление аналитики и прогресса',
                                   task='dashboard.tasks.front_params_update')
PeriodicTask.objects.get_or_create(interval=thirty_seconds_schedule,
                                   name='Проверка кол-ва задач на группе',
                                   task='dashboard.tasks.front_issues_count')
PeriodicTask.objects.get_or_create(interval=ten_minutes_schedule,
                                   name='Обновление отчета SL',
                                   task='naumen.tasks.update_service_level')
PeriodicTask.objects.get_or_create(interval=hour_schedule,
                                   name='Обновление отчета MTTR',
                                   task='naumen.tasks.update_mttr_level')
PeriodicTask.objects.get_or_create(interval=six_hours_schedule,
                                   name='Обновление отчета FLR',
                                   task='naumen.tasks.update_flr_level')
PeriodicTask.objects.get_or_create(interval=minute_schedule,
                                   name='Обновление первой линии',
                                   task='naumen.tasks.update_issues')
PeriodicTask.objects.get_or_create(interval=two_minutes_schedule,
                                   name='Обновление VIP линии',
                                   task='naumen.tasks.update_issues',
                                   kwargs=dumps({'is_vip': True}))
PeriodicTask.objects.get_or_create(
    interval=two_minutes_schedule,
    name='Проверка лимитов обрашений',
    task='naumen.tasks.check_issues_deadline_and_timer')
