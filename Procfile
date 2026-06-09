release: python manage.py migrate --noinput
web: gunicorn iatech.wsgi --bind 0.0.0.0:$PORT --log-file -
