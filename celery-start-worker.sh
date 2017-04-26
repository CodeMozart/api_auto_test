#!/usr/bin/env bash

# Need Celery, django-celery-results
# Starting the worker process, for Daemonization, see
# http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#daemonizing
celery -A auto_test worker -l info
