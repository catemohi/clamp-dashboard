from __future__ import absolute_import
import os
from json import dumps
from datetime import timedelta

from celery import Celery

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
# Создание переодических задач по умолчанию
app.conf.beat_schedule = {
    'Обновление аналитики и прогресса': {
        'task': 'dashboard.tasks.front_params_update',  # instead 'show'
        'schedule': timedelta(minutes=15),
    },
    'Проверка кол-ва задач на группе': {
        'task': 'dashboard.tasks.front_issues_count',  # instead 'show'
        'schedule': timedelta(seconds=30),
    },
    'Обновление отчета SL': {
        'task': 'naumen.tasks.update_service_level',  # instead 'show'
        'schedule': timedelta(minutes=10),
    },
    'Обновление отчета MTTR': {
        'task': 'naumen.tasks.update_mttr_level',  # instead 'show'
        'schedule': timedelta(hours=1),
    },
    'Обновление отчета FLR': {
        'task': 'naumen.tasks.update_flr_level',  # instead 'show'
        'schedule': timedelta(hours=6),
    },
    'Обновление первой линии': {
        'task': 'naumen.tasks.update_issues',  # instead 'show'
        'schedule': timedelta(minutes=1),
    },
    'Обновление VIP линии': {
        'task': 'naumen.tasks.update_issues',  # instead 'show'
        'schedule': timedelta(minutes=2),
        'kwargs': {'is_vip': True},
    },
    'Проверка лимитов обрашений': {
        'task': 'naumen.tasks.check_issues_deadline_and_timer',  # instead 'show'
        'schedule': timedelta(seconds=30),
    },
}
