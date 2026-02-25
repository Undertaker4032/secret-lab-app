#!/bin/bash
set -e

if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 0.5
    done
    echo "PostgreSQL is ready."
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec python -m gunicorn secret_lab.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info \
    --access-logfile - \
    --error-logfile -