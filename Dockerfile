from python:3.10-slim

COPY . /ao3_web_reader_django
WORKDIR /ao3_web_reader_django

RUN apt update && apt -y install nano curl

RUN curl -o /ao3_web_reader_django/static/libs/bootstrap.min.css  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css
RUN curl -o /ao3_web_reader_django/static/libs/bootstrap.bundle.min.js  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js

RUN pip3 install -r requirements.txt

RUN chmod +x scripts/entrypoint.sh
RUN chmod +x scripts/celery_beat_entrypoint.sh
RUN chmod +x scripts/celery_entrypoint.sh
