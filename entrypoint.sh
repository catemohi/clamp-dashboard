#!/bin/bash

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email test@test.ru
gunicorn --bind 0.0.0.0:8000 clamp.wsgi:application & \
daphne -b 0.0.0.0 -p 8001 clamp.asgi:application