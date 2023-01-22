#!/bin/bash
celery -A clamp worker -l info -c 1 -Q naumen_crud & \
celery -A clamp worker -l info -c 10 -Q main
