#!/bin/sh
set -e

echo "Starting..."

cd /code


if [ ! -f /run/secret ] ; then
    echo "Generating secret key"
    cat /dev/urandom | tr -dc 'a-zA-Z0-9~!@#$%^&*_()+}{?></";.,[]=-' | fold -w 32 | head -n 1 > /run/secret
    echo "Generated random:"
    cat /run/secret
fi

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate


# start nginx server
echo "Starting nginx webserver..."
nginx
echo "Started nginx webserver"

echo "Starting django server"
gunicorn -b 0.0.0.0:8080 --workers=2 --threads=4 --worker-class=gthread app.wsgi
