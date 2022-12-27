"""
Файл настроек Celery
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
from __future__ import absolute_import
import os
from celery import Celery

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
