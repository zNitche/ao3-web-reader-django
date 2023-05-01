from python:3.10-slim

COPY . /ao3_web_reader_django
WORKDIR /ao3_web_reader_django

RUN pip3 install -r requirements.txt

RUN chmod +x scripts/entrypoint.sh
RUN chmod +x scripts/celery_beat_entrypoint.sh
RUN chmod +x scripts/celery_entrypoint.sh
