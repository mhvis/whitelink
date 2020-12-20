#!/usr/bin/env bash
set -e
# Wait a little bit for database startup
sleep 2
python manage.py migrate --noinput
exec "$@"
