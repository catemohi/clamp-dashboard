from __future__ import absolute_import
import os
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
    'naumen.tasks.check_issue_deadline_and_timer': {'queue': 'main'},
    'naumen.tasks.check_issues_deadline_and_timer': {'queue': 'main'},
    'naumen.tasks.crud_issue': {'queue': 'main'},
    'naumen.tasks.*': {'queue': 'naumen_crud'},
    }
# загрузка tasks.py в приложение django
app.autodiscover_tasks()
# Создание переодических задач по умолчанию
app.conf.beat_schedule = {
    'Обновление аналитики и прогресса': {
        'task': 'dashboard.tasks.front_params_update',
        'schedule': timedelta(minutes=15),
    },
    'Проверка кол-ва задач на группе': {
        'task': 'dashboard.tasks.front_issues_count',
        'schedule': timedelta(seconds=30),
    },
    'Проверка лимитов обращений': {
        'task': 'naumen.tasks.check_issues_deadline_and_timer',
        'schedule': timedelta(seconds=30),
    },
    'Обновление отчета SL': {
        'task': 'naumen.tasks.update_service_level',
        'schedule': timedelta(minutes=10),
    },
    'Обновление отчета MTTR': {
        'task': 'naumen.tasks.update_mttr_level',
        'schedule': timedelta(hours=1),
    },
    'Обновление отчета FLR': {
        'task': 'naumen.tasks.update_flr_level',
        'schedule': timedelta(hours=6),
    },
    'Обновление первой линии': {
        'task': 'naumen.tasks.update_issues',
        'schedule': timedelta(minutes=2),
    },
    'Обновление VIP линии': {
        'task': 'naumen.tasks.update_issues',
        'schedule': timedelta(minutes=3),
        'kwargs': {'is_vip': True},
    },
    'Создание моделей настроек уведомлений о лимите обработки обращений': {
        'task': 'notification.tasks.create_burned_notification_models',
        'schedule': timedelta(seconds=30),
        'one_off': True,
    },
    'Создание моделей настроек уведомлений о возврате в работу обращений': {
        'task': 'notification.tasks.create_returned_notification_models',
        'schedule': timedelta(seconds=30),
        'one_off': True,
    },
}
