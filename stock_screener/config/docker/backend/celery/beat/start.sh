#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A src.core.celery_app.celery_app beat --loglevel=INFO