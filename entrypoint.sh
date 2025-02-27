#!/bin/sh

export DJANGO_SETTINGS_MODULE=theater.settings

python manage.py collectstatic --noinput

echo 'Applying migrations...'
python manage.py migrate

gunicorn theater.wsgi:application --bind 0.0.0.0:$PORT