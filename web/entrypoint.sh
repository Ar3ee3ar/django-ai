#!/bin/sh
# Fix permissions on staticfiles folder so appuser can write
chown -R appuser:appuser /app/staticfiles
chmod -R u+rwX /app/staticfiles

# Run migrations, collect static, then start Gunicorn
python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000