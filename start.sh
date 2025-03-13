#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ ! -f "db.sqlite3" ]; then
    echo "📌 База данных SQLite не найдена, создаем..."
else
    echo "✅ База данных SQLite уже существует."
fi

poetry run python manage.py migrate --noinput

echo "📂 Собираем статические файлы..."
poetry run python manage.py collectstatic --noinput

echo "🚀 Запускаем Gunicorn..."
exec poetry run gunicorn theater.wsgi:application --bind 0.0.0.0:8000
