#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
# python manage.py runserver 0.0.0.0:8000
gunicorn imageAPI.wsgi --bind=0.0.0.0:80

