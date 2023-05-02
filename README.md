## AO3 Web Reader

Reimplementation of [ao3-web-reader](https://github.com/zNitche/ao3-web-reader). 
This project won't be updated along with flask implementation.

---

### Technologies
- Django 4.2
- gunicorn
- nginx
- redis
- bootstrap
- celery

### Features
- Accounts authentication.
- Getting works from ao3.
- Grouping works using tags.
- Auto-update of added works.
- Downloading works.

### Setup
#### Dev
1. Generate `.env` config file
```
python3 generate_dotenv.py
```
2. Run dev docker services.
```
sudo docker compose -f docker-compose-dev.yml up
```
3. Run celery and celery beat workers
```
sh scripts/celery_entrypoint.sh
```
```
sh scripts/celery_beat_entrypoint.sh
```
#### Prod
1. Generate `.env` config file and change config values (`DB_PATH` and `LOGS_PATH`).
```
python3 generate_dotenv.py
```
2. Run docker services.
```
sudo docker compose up -d
```

#### Accounts Management
1. Bash into web app container.
```
sudo docker container exec -it ao3_web_reader_django bash
```
2. Run accounts manager cli `python3 manage.py create_user`.

#### Tests
App contains some example tests for available apps. To run them:
```
python3 manage.py test
```
