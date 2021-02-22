#!/bin/sh
set -e

echo "Starting..."

cd /code


python manage.py makemigrations
python manage.py migrate

# Start the management command
python manage.py runserver 0.0.0.0:8080
