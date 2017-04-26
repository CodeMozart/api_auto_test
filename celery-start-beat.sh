#!/usr/bin/env bash

# Need  django-celery-beat
# Start the celery beat service using the django scheduler
celery -A auto_test beat -l info -S django
