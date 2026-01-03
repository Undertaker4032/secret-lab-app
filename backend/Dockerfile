FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=secret_lab.settings

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        curl \
        netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn==21.2.0

RUN which gunicorn || echo "gunicorn not found in PATH"
RUN python -c "import gunicorn; print(f'Gunicorn version: {gunicorn.__version__}')"

COPY . .

RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Ждем базу\n\
if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then\n\
    echo "Waiting for PostgreSQL..."\n\
    while ! nc -z $DB_HOST $DB_PORT; do\n\
        sleep 0.5\n\
    done\n\
    echo "PostgreSQL started"\n\
fi\n\
\n\
# Миграции\n\
python manage.py migrate --noinput\n\
\n\
# Собираем статику\n\
python manage.py collectstatic --noinput --clear\n\
\n\
# Запускаем gunicorn (используем python -m для гарантии)\n\
exec python -m gunicorn secret_lab.wsgi:application \\\n\
    --bind 0.0.0.0:8000 \\\n\
    --workers 3 \\\n\
    --log-level info \\\n\
    --access-logfile - \\\n\
    --error-logfile -' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]