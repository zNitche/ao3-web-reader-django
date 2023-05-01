python manage.py migrate --no-input
#python manage.py collectstatic --no-input

gunicorn -c gunicorn.conf.py ao3_web_reader_django.wsgi --preload