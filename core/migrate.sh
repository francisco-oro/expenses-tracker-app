# !/bin/bash
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"francisco.oro@comunidad.unam.mx"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput

/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true