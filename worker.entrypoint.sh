#!/bin/bash
celery -A clamp worker -l error -c 1 -Q naumen_crud & \
celery -A clamp worker -l error -c 10 -Q celery
