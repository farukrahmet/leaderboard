#!/bin/bash

python manage.py migrate
python manage.py fill_users_cache

/usr/local/bin/gunicorn leaderboard.wsgi:application \
    --workers 4 \
    --bind :$APPLICATION_PORT \
    -k gevent
    --capture-output --preload