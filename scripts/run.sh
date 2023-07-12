#!/bin/bash

set -c

python3 manage.py wait_for_db
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate

uswgi --socket :9000 --workers 4 --master --enable-threads --module core.wsgi