#!/bin/bash

set -o errexit
set -o nounset

celery -A src.core.celery_app.celery_app worker --loglevel=INFO